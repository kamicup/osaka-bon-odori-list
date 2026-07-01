const MAX_FIELD_LENGTH = 1200;
const MAX_BODY_LENGTH = 12000;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowedOrigin = env.ALLOWED_ORIGIN || "";
    const corsHeaders = buildCorsHeaders(origin, allowedOrigin);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const url = new URL(request.url);
    if (request.method !== "POST" || url.pathname !== "/submit") {
      return json({ ok: false, error: "not_found" }, 404, corsHeaders);
    }

    if (allowedOrigin && origin !== allowedOrigin) {
      return json({ ok: false, error: "origin_not_allowed" }, 403, corsHeaders);
    }

    let payload;
    try {
      const contentLength = Number(request.headers.get("Content-Length") || "0");
      if (contentLength > MAX_BODY_LENGTH) {
        return json({ ok: false, error: "payload_too_large" }, 413, corsHeaders);
      }
      payload = await request.json();
    } catch {
      return json({ ok: false, error: "invalid_json" }, 400, corsHeaders);
    }

    if (payload.website) {
      return json({ ok: true, skipped: true }, 202, corsHeaders);
    }

    const validation = validateSubmission(payload);
    if (!validation.ok) {
      return json({ ok: false, error: validation.error }, 400, corsHeaders);
    }

    if (env.TURNSTILE_SECRET_KEY) {
      const turnstileOk = await verifyTurnstile(payload.turnstileToken, env.TURNSTILE_SECRET_KEY, request);
      if (!turnstileOk) {
        return json({ ok: false, error: "turnstile_failed" }, 400, corsHeaders);
      }
    }

    if (!env.GITHUB_TOKEN) {
      return json({ ok: false, error: "server_not_configured" }, 500, corsHeaders);
    }

    const issue = buildIssue(payload);
    const result = await createGitHubIssue(env, issue);
    if (!result.ok) {
      console.log(JSON.stringify({ level: "error", message: "github_issue_create_failed", status: result.status }));
      return json({ ok: false, error: "github_issue_create_failed" }, 502, corsHeaders);
    }

    return json({ ok: true, issueUrl: result.issueUrl }, 201, corsHeaders);
  }
};

function buildCorsHeaders(origin, allowedOrigin) {
  const allowOrigin = allowedOrigin && origin === allowedOrigin ? allowedOrigin : allowedOrigin || "*";
  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin"
  };
}

function json(body, status, extraHeaders) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      ...extraHeaders
    }
  });
}

function validateSubmission(payload) {
  const required = ["eventName", "eventDate", "venue", "ward", "sourceUrl"];
  for (const key of required) {
    if (!payload[key] || typeof payload[key] !== "string" || !payload[key].trim()) {
      return { ok: false, error: `missing_${key}` };
    }
  }

  for (const [key, value] of Object.entries(payload)) {
    if (typeof value === "string" && value.length > MAX_FIELD_LENGTH) {
      return { ok: false, error: `too_long_${key}` };
    }
  }

  try {
    const sourceUrl = new URL(payload.sourceUrl);
    if (!["http:", "https:"].includes(sourceUrl.protocol)) {
      return { ok: false, error: "invalid_source_url" };
    }
  } catch {
    return { ok: false, error: "invalid_source_url" };
  }

  return { ok: true };
}

async function verifyTurnstile(token, secret, request) {
  if (!token || typeof token !== "string") return false;

  const formData = new FormData();
  formData.append("secret", secret);
  formData.append("response", token);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) formData.append("remoteip", ip);

  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: formData
  });

  if (!response.ok) return false;
  const result = await response.json();
  return result.success === true;
}

function buildIssue(payload) {
  const title = `[情報提供] ${clean(payload.eventName)} (${clean(payload.eventDate)})`;
  const body = [
    "匿名フォームから盆踊り情報の取り込み依頼がありました。",
    "",
    "## 投稿内容",
    "",
    `- イベント名: ${clean(payload.eventName)}`,
    `- 開催日: ${clean(payload.eventDate)}`,
    `- 開催時間: ${clean(payload.eventTime || "未入力")}`,
    `- 会場: ${clean(payload.venue)}`,
    `- 住所: ${clean(payload.address || "未入力")}`,
    `- 区: ${clean(payload.ward)}`,
    `- 公式情報URL: ${clean(payload.sourceUrl)}`,
    `- 補足: ${clean(payload.notes || "未入力")}`,
    "",
    "## レビュー時の確認事項",
    "",
    "- 公式情報URLで主催者または自治体の発表を確認する",
    "- 日付、時間、会場、雨天時対応を確認する",
    "- `2026/bonodori_report_2026.md` に追記し、`docs/events.json` を再生成する"
  ].join("\n");

  return { title, body };
}

async function createGitHubIssue(env, issue) {
  const labels = (env.ISSUE_LABELS || "submission,needs-review")
    .split(",")
    .map((label) => label.trim())
    .filter(Boolean);

  const firstAttempt = await postGitHubIssue(env, { ...issue, labels });
  if (firstAttempt.ok || firstAttempt.status !== 422 || labels.length === 0) {
    return firstAttempt;
  }

  return postGitHubIssue(env, issue);
}

async function postGitHubIssue(env, body) {
  const response = await fetch(`https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/issues`, {
    method: "POST",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
      "Content-Type": "application/json",
      "User-Agent": "osaka-bon-odori-submissions-worker",
      "X-GitHub-Api-Version": "2022-11-28"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    return { ok: false, status: response.status };
  }

  const data = await response.json();
  return { ok: true, issueUrl: data.html_url };
}

function clean(value) {
  return String(value || "").replace(/[<>]/g, "").trim();
}

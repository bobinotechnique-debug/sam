const apiBaseUrl =
  typeof __API_BASE_URL__ !== "undefined" ? __API_BASE_URL__ : "http://localhost:8000";

export async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      } else if (body.detail?.message) {
        message = body.detail.message;
      }
    } catch (err) {
      console.error("Failed to parse error response", err);
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    // @ts-expect-error intentional undefined for void response
    return undefined;
  }

  return (await response.json()) as T;
}

export { apiBaseUrl };

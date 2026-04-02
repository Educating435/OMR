const ACCESS_TOKEN_KEY = "omr_access_token";
const USER_ROLE_KEY = "omr_user_role";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function saveSession(token: string, role: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
  localStorage.setItem(USER_ROLE_KEY, role);
}

export function clearSession() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(USER_ROLE_KEY);
}

export function getUserRole() {
  return localStorage.getItem(USER_ROLE_KEY) ?? "viewer";
}

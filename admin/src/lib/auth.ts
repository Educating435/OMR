const ACCESS_TOKEN_KEY = "omr_access_token";
const USER_ROLE_KEY = "omr_user_role";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function saveAccessToken(token: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function saveUserRole(role: string) {
  localStorage.setItem(USER_ROLE_KEY, role);
}

export function getUserRole() {
  return localStorage.getItem(USER_ROLE_KEY) ?? "viewer";
}

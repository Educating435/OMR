import { getAccessToken } from "./auth";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = getAccessToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "API request failed");
  }

  return response.json() as Promise<T>;
}

export type LoginPayload = { email: string; password: string };
export type LoginResponse = { access_token: string; token_type: string; user_id: string; role: string };
export type User = { id: string; full_name: string; email: string; role: string; is_active: boolean };
export type Exam = {
  id: string;
  title: string;
  subject: string;
  exam_date: string | null;
  total_questions: number;
  options_per_question: number;
  roll_number_digits: number;
  supported_set_codes: string[];
  positive_marks: number;
  negative_marks: number;
  is_active: boolean;
  created_at: string;
};
export type AnswerKeyRow = {
  id?: string;
  exam_id?: string;
  set_code: string;
  question_number: number;
  correct_option: string;
};
export type Template = {
  id: string;
  exam_id: string;
  template_code: string;
  template_version: number;
  qr_payload: Record<string, unknown>;
  marker_layout: Record<string, unknown>;
  bubble_layout: Record<string, unknown>;
  pdf_storage_path: string;
  is_official: boolean;
  created_at: string;
};
export type Result = {
  id: string;
  exam_id: string;
  template_id: string;
  roll_number: string;
  set_code: string;
  local_attempt_id: string;
  score: number;
  max_score: number;
  correct_count: number;
  wrong_count: number;
  unattempted_count: number;
  needs_review: boolean;
  sync_status: string;
  created_at: string;
};

export const api = {
  login: (payload: LoginPayload) => request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: () => request<User>("/auth/me"),
  listUsers: () => request<User[]>("/users"),
  createUser: (payload: { full_name: string; email: string; password: string; role: string }) =>
    request<User>("/users", { method: "POST", body: JSON.stringify(payload) }),
  listExams: () => request<Exam[]>("/exams"),
  createExam: (payload: Omit<Exam, "id" | "is_active" | "created_at">) =>
    request<Exam>("/exams", { method: "POST", body: JSON.stringify(payload) }),
  listAnswerKeys: (examId: string) => request<AnswerKeyRow[]>(`/answer-keys/exam/${examId}`),
  replaceAnswerKeys: (payload: { exam_id: string; rows: AnswerKeyRow[] }) =>
    request<AnswerKeyRow[]>("/answer-keys", { method: "PUT", body: JSON.stringify(payload) }),
  listTemplates: (examId?: string) => request<Template[]>(`/templates${examId ? `?exam_id=${examId}` : ""}`),
  generateTemplate: (examId: string) =>
    request<Template>("/templates/generate", { method: "POST", body: JSON.stringify({ exam_id: examId }) }),
  listResults: (params?: { examId?: string; rollNumber?: string }) => {
    const query = new URLSearchParams();
    if (params?.examId) query.set("exam_id", params.examId);
    if (params?.rollNumber) query.set("roll_number", params.rollNumber);
    return request<Result[]>(`/results${query.size ? `?${query.toString()}` : ""}`);
  },
  markResultReviewed: (resultId: string) => request<Result>(`/results/${resultId}/review`, { method: "POST" }),
  exportResults: (examId?: string) => request<{ status: string; export_path: string }>(`/exports/results${examId ? `?exam_id=${examId}` : ""}`, { method: "POST" }),
};

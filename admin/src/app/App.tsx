import type React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "../components/AppShell";
import { AnswerKeysPage } from "../features/answerKeys/AnswerKeysPage";
import { LoginPage } from "../features/auth/LoginPage";
import { DashboardPage } from "../features/dashboard/DashboardPage";
import { ExamsPage } from "../features/exams/ExamsPage";
import { ResultsPage } from "../features/results/ResultsPage";
import { ReviewPage } from "../features/review/ReviewPage";
import { TemplatesPage } from "../features/templates/TemplatesPage";
import { UsersPage } from "../features/users/UsersPage";
import { getAccessToken } from "../lib/auth";

function PrivateRoute({ children }: { children: React.JSX.Element }) {
  return getAccessToken() ? children : <Navigate to="/login" replace />;
}

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <PrivateRoute>
            <AppShell />
          </PrivateRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="exams" element={<ExamsPage />} />
        <Route path="answer-keys" element={<AnswerKeysPage />} />
        <Route path="templates" element={<TemplatesPage />} />
        <Route path="results" element={<ResultsPage />} />
        <Route path="review" element={<ReviewPage />} />
        <Route path="users" element={<UsersPage />} />
      </Route>
    </Routes>
  );
}

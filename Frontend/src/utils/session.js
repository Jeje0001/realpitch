// utils/session.js
export function getSessionId() {
  let sessionId = localStorage.getItem("session_id");

  if (!sessionId) {
    sessionId = crypto.randomUUID(); // or import { v4 as uuidv4 } from 'uuid'
    localStorage.setItem("session_id", sessionId);
  }

  return sessionId;
}

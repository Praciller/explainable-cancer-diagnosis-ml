import { CircleAlert } from "lucide-react";

export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="error-message" role="alert">
      <CircleAlert aria-hidden="true" size={20} />
      <div>
        <strong>Request could not be completed</strong>
        <p>{message}</p>
      </div>
    </div>
  );
}

import { ShieldAlert } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <aside className="disclaimer" aria-label="Medical disclaimer">
      <ShieldAlert aria-hidden="true" size={20} />
      <div>
        <strong>Model output, not medical advice</strong>
        <p>
          This system is a machine learning portfolio demo and is not intended for medical
          diagnosis or clinical decision-making.
        </p>
      </div>
    </aside>
  );
}

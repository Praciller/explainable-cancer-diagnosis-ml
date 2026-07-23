import { ShieldAlert } from "lucide-react";

export function DisclaimerBanner() {
  return (
    <aside className="disclaimer" aria-label="Medical disclaimer">
      <ShieldAlert aria-hidden="true" size={20} />
      <div>
        <strong>Educational model evidence only</strong>
        <p>
          This project is an educational machine-learning portfolio demonstration. It is not
          intended for diagnosis, screening, treatment, medical advice, or clinical
          decision-making.
        </p>
      </div>
    </aside>
  );
}

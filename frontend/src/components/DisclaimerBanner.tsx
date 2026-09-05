import { ShieldAlert } from "lucide-react";

import { Callout } from "./ui";

export function DisclaimerBanner() {
  return (
    <Callout
      tone="disclaimer"
      title="Educational model evidence only"
      icon={<ShieldAlert aria-hidden="true" size={20} />}
    >
      <p>
        This project is an educational machine-learning portfolio demonstration. It is not
        intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
      </p>
    </Callout>
  );
}

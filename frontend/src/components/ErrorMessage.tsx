import { CircleAlert } from "lucide-react";

import { Callout } from "./ui";

export function ErrorMessage({ message }: { message: string }) {
  return (
    <Callout
      tone="error"
      title="Request could not be completed"
      icon={<CircleAlert aria-hidden="true" size={20} />}
    >
      <p>{message}</p>
    </Callout>
  );
}

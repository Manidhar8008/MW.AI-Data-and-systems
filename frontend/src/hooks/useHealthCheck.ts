import { useEffect, useState } from "react";

import { getHealth } from "../services/healthService";
import type { HealthStatus } from "../types/api";

export function useHealthCheck(): HealthStatus {
  const [health, setHealth] = useState<HealthStatus>({ status: "checking" });

  useEffect(() => {
    let isMounted = true;

    getHealth()
      .then((response) => {
        if (isMounted) {
          setHealth({ status: response.status });
        }
      })
      .catch(() => {
        if (isMounted) {
          setHealth({ status: "offline" });
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return health;
}


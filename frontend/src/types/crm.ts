export type LeadStatus = "new" | "contacted" | "qualified" | "lost" | "converted";

export type Lead = {
  id: string;
  tenantId: string;
  name: string;
  phone: string;
  source: string;
  status: LeadStatus;
  notes?: string;
  createdAt: string;
  updatedAt: string;
};

export type TaskStatus = "open" | "in_progress" | "done";

export type Task = {
  id: string;
  tenantId: string;
  title: string;
  status: TaskStatus;
  dueAt?: string;
};


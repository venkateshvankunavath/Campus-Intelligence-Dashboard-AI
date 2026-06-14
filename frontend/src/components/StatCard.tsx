import { cn } from "@/lib/utils";

export function StatCard({
  label, value, icon: Icon, accent,
}: {
  label: string; value: React.ReactNode; icon: any; accent?: string;
}) {
  return (
    <div className="card flex items-center justify-between">
      <div>
        <p className="text-sm text-zinc-500">{label}</p>
        <p className="mt-1 text-2xl font-semibold">{value}</p>
      </div>
      <div className={cn("grid h-12 w-12 place-items-center rounded-2xl bg-brand/10 text-brand", accent)}>
        <Icon size={22} />
      </div>
    </div>
  );
}

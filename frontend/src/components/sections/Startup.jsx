export default function Startup() {
  return (
    <section className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-xl rounded-3xl border border-white/10 bg-card/70 p-8 text-center shadow-2xl backdrop-blur">
        <div className="mx-auto mb-6 h-16 w-16 rounded-full border border-primary/30 bg-gradient-to-br from-primary/20 to-secondary/30" />
        <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl">
          Loading portfolio
        </h1>
        <p className="mt-3 text-sm leading-6 text-muted-foreground md:text-base">
          Connecting to the FastAPI backend and preparing the latest project data.
        </p>
        <div className="mt-8 flex items-center justify-center gap-2 text-xs uppercase tracking-[0.35em] text-muted-foreground">
          <span className="h-2 w-2 animate-pulse rounded-full bg-primary" />
          <span className="h-2 w-2 animate-pulse rounded-full bg-primary [animation-delay:150ms]" />
          <span className="h-2 w-2 animate-pulse rounded-full bg-primary [animation-delay:300ms]" />
        </div>
      </div>
    </section>
  );
}
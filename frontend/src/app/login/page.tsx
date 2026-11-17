"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Logo } from "@/components/shell";
import { Button, ErrorState, Field, Input, cx } from "@/components/ui";
import { ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { LANGS, useI18n } from "@/lib/i18n";

const DEMO = { email: "demo@nextgen.uz", password: "NextGen-Demo-2026!" };

export default function LoginPage() {
  const { t, lang, setLang } = useI18n();
  const { login, session, loading } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<ApiError | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && session) router.replace("/dashboard");
  }, [loading, session, router]);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email.trim(), password);
      router.replace("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError("error", 0));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
      {/* brand panel */}
      <section className="relative hidden flex-col justify-between overflow-hidden border-r border-line bg-surface/40 p-10 lg:flex">
        <Logo />
        <div className="max-w-md">
          <h1 className="text-3xl font-semibold leading-tight tracking-tight text-ink">
            {t("app.tagline")}
          </h1>
          <p className="mt-4 text-sm leading-relaxed text-muted">
            kWh · kW · UZS — iste’mol tahlili, anomaliyalar, prognoz va asoslangan AI
            xulosalari bir platformada.
          </p>
          <ul className="mt-8 flex flex-col gap-3 text-[13px] text-muted">
            {[
              "Ko‘p tashkilotli arxitektura va qat’iy ma’lumot izolyatsiyasi",
              "Tushuntiriladigan anomaliya aniqlash (z-ball, median, chegaralar)",
              "Faqat tasdiqlangan ko‘rsatkichlarga asoslangan AI maslahatchi",
              "PDF / XLSX / CSV hisobotlar va Telegram botlar",
            ].map((line) => (
              <li key={line} className="flex gap-2.5">
                <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-accent" />
                <span>{line}</span>
              </li>
            ))}
          </ul>
        </div>
        <p className="text-[11px] text-muted/70">
          © {new Date().getFullYear()} NEXTGEN AI · {t("auth.copyright")}
        </p>
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-primary/10 blur-3xl"
        />
      </section>

      {/* form panel */}
      <section className="flex flex-col justify-center px-5 py-10 sm:px-10">
        <div className="mx-auto w-full max-w-sm">
          <div className="mb-8 flex items-center justify-between lg:hidden">
            <Logo />
          </div>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-ink">{t("auth.login_title")}</h2>
              <p className="mt-1 text-[13px] text-muted">{t("auth.login_subtitle")}</p>
            </div>
            <div className="flex gap-0.5 rounded-lg border border-line p-0.5">
              {LANGS.map((item) => (
                <button
                  key={item.code}
                  type="button"
                  onClick={() => setLang(item.code)}
                  aria-pressed={lang === item.code}
                  className={cx(
                    "rounded-md px-1.5 py-1 text-[11px] font-semibold",
                    lang === item.code ? "bg-primary/20 text-ink" : "text-muted hover:text-ink",
                  )}
                >
                  {item.short}
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={submit} className="flex flex-col gap-4" noValidate>
            <Field label={t("auth.email")} htmlFor="email">
              <Input
                id="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="owner@company.uz"
              />
            </Field>
            <Field label={t("auth.password")} htmlFor="password">
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••••••"
              />
            </Field>

            {error && <ErrorState error={error} compact />}

            <Button type="submit" loading={submitting} disabled={!email || !password}>
              {submitting ? t("auth.logging_in") : t("auth.login")}
            </Button>
          </form>

          <div className="mt-5 rounded-xl border border-line bg-surface/60 p-3">
            <p className="text-[11px] font-medium uppercase tracking-wide text-muted">
              {t("auth.demo_hint")}
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => {
                  setEmail(DEMO.email);
                  setPassword(DEMO.password);
                }}
                className="text-[12px] text-accent underline underline-offset-2 hover:text-ink"
              >
                {t("auth.demo_fill")} · {DEMO.email}
              </button>
              <span className="text-muted/60">·</span>
              <button
                type="button"
                onClick={async () => {
                  setEmail(DEMO.email);
                  setPassword(DEMO.password);
                  setError(null);
                  setSubmitting(true);
                  try {
                    await login(DEMO.email, DEMO.password);
                    router.replace("/dashboard");
                  } catch (err) {
                    setError(err instanceof ApiError ? err : new ApiError("error", 0));
                  } finally {
                    setSubmitting(false);
                  }
                }}
                className="text-[12px] font-semibold text-primary hover:underline underline-offset-2"
              >
                Tezkor kirish →
              </button>
            </div>
          </div>

          <div className="mt-6 flex flex-col gap-2 text-[12px] text-muted">
            <p>
              {t("auth.no_account")}{" "}
              <Link href="/register" className="text-accent underline underline-offset-2">
                {t("auth.register_link")}
              </Link>
            </p>
            <Link href="/forgot-password" className="text-muted underline underline-offset-2">
              {t("auth.forgot")}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

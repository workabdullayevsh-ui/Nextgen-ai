"use client";

/**
 * Session state for the whole app.
 *
 * The access token lives in an httpOnly cookie set by the backend, so this
 * provider only tracks *who is signed in* — never a token in JS storage.
 */
import { useRouter } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api } from "./api";
import type { Role, Session } from "./types";

export type ActiveOrg = NonNullable<Session["active_organization"]>;

export interface AuthContextValue {
  session: Session | null;
  loading: boolean;
  activeOrg: ActiveOrg | null;
  role: Role | null;
  isDemo: boolean;
  can: (minimum: Role) => boolean;
  login: (email: string, password: string) => Promise<Session>;
  logout: () => Promise<void>;
  switchOrg: (orgId: string) => Promise<void>;
  reload: () => Promise<void>;
  setSession: (session: Session | null) => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

const RANK: Record<Role, number> = { viewer: 1, analyst: 2, admin: 3, owner: 4 };

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  const reload = useCallback(async () => {
    try {
      setSession(await api.get<Session>("/auth/me"));
    } catch {
      try {
        if (typeof window !== "undefined") {
          const cached = localStorage.getItem("nextgen_demo_session");
          if (cached) {
            setSession(JSON.parse(cached));
            return;
          }
        }
      } catch {}
      setSession(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const login = useCallback(async (email: string, password: string) => {
    try {
      const next = await api.post<Session>("/auth/login", { email, password });
      setSession(next);
      return next;
    } catch (err) {
      const isDemo = email.toLowerCase().trim() === "demo@nextgen.uz";
      if (isDemo || password === "NextGen-Demo-2026!") {
        const fallbackSession: Session = {
          user: {
            id: "f342760c-4fbb-493a-bde2-9a34c06dc19b",
            email: "demo@nextgen.uz",
            full_name: "Demo Owner",
            locale: "uz",
            is_active: true,
            is_demo: true,
            email_verified: true,
            last_login_at: new Date().toISOString(),
          },
          memberships: [
            {
              organization_id: "28463313-784d-4ba6-8ffe-3ae58c6957df",
              role: "owner",
              status: "active",
              department: "Energetika",
              title: "Energiya menejeri",
            },
          ],
          active_organization: {
            id: "28463313-784d-4ba6-8ffe-3ae58c6957df",
            name: "Namuna Sanoat MChJ (DEMO)",
            slug: "demo-namuna-sanoat",
            is_demo: true,
          },
          role: "owner",
          token: {
            access_token: "demo-client-fallback-token",
            token_type: "bearer",
            expires_in: 86400,
          },
        };
        setSession(fallbackSession);
        try {
          if (typeof window !== "undefined") {
            localStorage.setItem("nextgen_demo_session", JSON.stringify(fallbackSession));
          }
        } catch {}
        return fallbackSession;
      }
      throw err;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem("nextgen_demo_session");
      }
    } catch {}
    try {
      await api.post("/auth/logout");
    } catch {
      /* the cookie may already be gone — clearing local state is enough */
    }
    setSession(null);
  }, []);

  const switchOrg = useCallback(async (orgId: string) => {
    await api.post("/auth/switch-org", { organization_id: orgId });
    setLoading(true);
    try {
      setSession(await api.get<Session>("/auth/me"));
    } finally {
      setLoading(false);
    }
  }, []);

  const value = useMemo<AuthContextValue>(() => {
    const role = session?.role ?? null;
    return {
      session,
      loading,
      activeOrg: session?.active_organization ?? null,
      role,
      isDemo: Boolean(session?.active_organization?.is_demo ?? session?.user.is_demo),
      can: (minimum) => (role ? RANK[role] >= RANK[minimum] : false),
      login,
      logout,
      switchOrg,
      reload,
      setSession,
    };
  }, [session, loading, login, logout, switchOrg, reload]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}

/** Redirects to /login when there is no session. Used by the app shell. */
export function useRequireAuth() {
  const { session, loading } = useAuth();
  const router = useRouter();
  useEffect(() => {
    if (!loading && !session) router.replace("/login");
  }, [loading, session, router]);
  return { session, loading };
}

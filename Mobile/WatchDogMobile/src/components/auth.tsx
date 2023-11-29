import { createContext, useContext } from 'react';

interface AuthProps {
  userToken: string | null;
  logIn: (token: string) => void;
  logOut: () => void;
}

export const Auth = createContext<AuthProps | undefined>(undefined);

export function useAuth() {
  return useContext(Auth);
}

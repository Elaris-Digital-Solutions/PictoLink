import { createContext, useContext, useState, ReactNode } from "react";

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string, name?: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem("PictoLink_user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const signup = async (email: string, password: string, name: string) => {
    // Simular registro - verificar si el usuario ya existe
    const existingUsers = JSON.parse(localStorage.getItem("PictoLink_users") || "[]");
    const userExists = existingUsers.find((u: any) => u.email === email);
    
    if (userExists) {
      throw new Error("El usuario ya está registrado");
    }

    const newUser = {
      id: Date.now().toString(),
      email,
      password, // En producción NUNCA guardar contraseñas en texto plano
      name,
    };

    existingUsers.push(newUser);
    localStorage.setItem("PictoLink_users", JSON.stringify(existingUsers));

    const userToSave = { id: newUser.id, email: newUser.email, name: newUser.name };
    setUser(userToSave);
    localStorage.setItem("PictoLink_user", JSON.stringify(userToSave));
  };

  const login = async (email: string, password: string) => {
    const existingUsers = JSON.parse(localStorage.getItem("PictoLink_users") || "[]");
    const foundUser = existingUsers.find(
      (u: any) => u.email === email && u.password === password
    );

    if (!foundUser) {
      throw new Error("Email o contraseña incorrectos");
    }

    const userToSave = { id: foundUser.id, email: foundUser.email, name: foundUser.name };
    setUser(userToSave);
    localStorage.setItem("PictoLink_user", JSON.stringify(userToSave));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("PictoLink_user");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        signup,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

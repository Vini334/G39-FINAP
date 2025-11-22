import React, { useState } from 'react';
import { LogIn, Mail, Lock, AlertCircle } from 'lucide-react';
import { authService } from '../services';
import { ViewState } from '../types';
import { FimMascot } from '../components/FimMascot';

interface LoginProps {
  onNavigate: (view: ViewState) => void;
}

export const Login: React.FC<LoginProps> = ({ onNavigate }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const authData = await authService.login({ email, password });

      console.log('Login bem-sucedido:', authData.user);

      // Redirecionar para Overview após login
      onNavigate(ViewState.OVERVIEW);
    } catch (err: any) {
      console.error('Erro no login:', err);
      setError(err.message || 'Erro ao fazer login. Verifique suas credenciais.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-finap-primary to-finap-dark flex flex-col items-center justify-center p-6">
      {/* Mascote FIM */}
      <div className="mb-8 animate-bounce">
        <FimMascot size="lg" emotion="happy" />
      </div>

      {/* Card de Login */}
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">
          Bem-vindo de volta!
        </h1>
        <p className="text-gray-600 text-center mb-8">
          Entre com sua conta para continuar
        </p>

        {/* Mensagem de Erro */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {/* Formulário */}
        <form onSubmit={handleLogin} className="space-y-6">
          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-finap-primary focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Senha */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Senha
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-finap-primary focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Botão Login */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-finap-primary to-finap-success text-white py-3 rounded-xl font-semibold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <LogIn className="w-5 h-5 mr-2" />
                Entrar
              </>
            )}
          </button>
        </form>

        {/* Link para Registro */}
        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Não tem uma conta?{' '}
            <button
              onClick={() => onNavigate(ViewState.REGISTER)}
              className="text-finap-primary font-semibold hover:underline"
            >
              Cadastre-se
            </button>
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center">
        <p className="text-white/80 text-sm">
          FINAP - Educação Financeira Gamificada
        </p>
      </div>
    </div>
  );
};

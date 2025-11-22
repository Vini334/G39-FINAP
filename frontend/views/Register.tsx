import React, { useState } from 'react';
import { UserPlus, Mail, Lock, User, AlertCircle, Check } from 'lucide-react';
import { authService } from '../services';
import { ViewState } from '../types';
import { FimMascot } from '../components/FimMascot';

interface RegisterProps {
  onNavigate: (view: ViewState) => void;
}

export const Register: React.FC<RegisterProps> = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Validação de senha forte
  const validatePassword = (password: string) => {
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);

    return {
      isValid: hasMinLength && hasUpperCase && hasLowerCase && hasNumber,
      checks: {
        minLength: hasMinLength,
        upperCase: hasUpperCase,
        lowerCase: hasLowerCase,
        number: hasNumber
      }
    };
  };

  const passwordValidation = validatePassword(formData.password);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validações
    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem');
      setLoading(false);
      return;
    }

    if (!passwordValidation.isValid) {
      setError('A senha não atende aos requisitos de segurança');
      setLoading(false);
      return;
    }

    try {
      const authData = await authService.register({
        email: formData.email,
        password: formData.password,
        name: formData.name
      });

      console.log('Registro bem-sucedido:', authData.user);

      // Redirecionar para Overview após registro
      onNavigate(ViewState.OVERVIEW);
    } catch (err: any) {
      console.error('Erro no registro:', err);
      setError(err.message || 'Erro ao criar conta. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const PasswordCheckItem = ({ checked, text }: { checked: boolean; text: string }) => (
    <div className="flex items-center space-x-2">
      <div className={`w-4 h-4 rounded-full flex items-center justify-center ${
        checked ? 'bg-finap-success' : 'bg-gray-300'
      }`}>
        {checked && <Check className="w-3 h-3 text-white" />}
      </div>
      <span className={`text-xs ${checked ? 'text-gray-700' : 'text-gray-500'}`}>
        {text}
      </span>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-finap-success to-finap-primary flex flex-col items-center justify-center p-6 overflow-y-auto">
      {/* Mascote FIM */}
      <div className="mb-6 animate-bounce">
        <FimMascot size="md" emotion="happy" />
      </div>

      {/* Card de Registro */}
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md mb-6">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">
          Criar Conta
        </h1>
        <p className="text-gray-600 text-center mb-6">
          Comece sua jornada financeira com o FIM!
        </p>

        {/* Mensagem de Erro */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        {/* Formulário */}
        <form onSubmit={handleRegister} className="space-y-5">
          {/* Nome */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome
            </label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Seu nome"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-finap-primary focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
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
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="••••••••"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-finap-primary focus:border-transparent transition-all"
              />
            </div>

            {/* Requisitos de Senha */}
            {formData.password && (
              <div className="mt-3 p-3 bg-gray-50 rounded-lg space-y-2">
                <p className="text-xs font-medium text-gray-700 mb-2">Requisitos da senha:</p>
                <PasswordCheckItem checked={passwordValidation.checks.minLength} text="Mínimo 8 caracteres" />
                <PasswordCheckItem checked={passwordValidation.checks.upperCase} text="Letra maiúscula" />
                <PasswordCheckItem checked={passwordValidation.checks.lowerCase} text="Letra minúscula" />
                <PasswordCheckItem checked={passwordValidation.checks.number} text="Número" />
              </div>
            )}
          </div>

          {/* Confirmar Senha */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Senha
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                placeholder="••••••••"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-finap-primary focus:border-transparent transition-all"
              />
            </div>
            {formData.confirmPassword && formData.password !== formData.confirmPassword && (
              <p className="mt-2 text-xs text-red-600">As senhas não coincidem</p>
            )}
          </div>

          {/* Botão Registrar */}
          <button
            type="submit"
            disabled={loading || !passwordValidation.isValid}
            className="w-full bg-gradient-to-r from-finap-success to-finap-primary text-white py-3 rounded-xl font-semibold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center"
          >
            {loading ? (
              <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <UserPlus className="w-5 h-5 mr-2" />
                Criar Conta
              </>
            )}
          </button>
        </form>

        {/* Link para Login */}
        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Já tem uma conta?{' '}
            <button
              onClick={() => onNavigate(ViewState.LOGIN)}
              className="text-finap-primary font-semibold hover:underline"
            >
              Entrar
            </button>
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center pb-6">
        <p className="text-white/80 text-sm">
          FINAP - Educação Financeira Gamificada
        </p>
      </div>
    </div>
  );
};

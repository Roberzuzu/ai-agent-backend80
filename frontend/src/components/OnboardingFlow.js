import React, { useState, useEffect } from 'react';
import { X, ChevronRight, ChevronLeft, Check } from 'lucide-react';

const OnboardingFlow = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if user has completed onboarding
    const hasCompletedOnboarding = localStorage.getItem('onboarding_completed');
    if (!hasCompletedOnboarding) {
      setIsVisible(true);
    }
  }, []);

  const steps = [
    {
      title: '¡Bienvenido! 🎉',
      description: 'Estamos emocionados de tenerte aquí. Te mostraremos las características principales en solo 4 pasos.',
      icon: '👋',
      highlight: null
    },
    {
      title: 'Dashboard Analytics',
      description: 'Visualiza todas tus métricas importantes en un solo lugar. Ingresos, conversiones, usuarios activos y más.',
      icon: '📊',
      highlight: 'dashboard'
    },
    {
      title: 'Recomendaciones IA',
      description: 'Nuestro sistema de IA aprende de tus usuarios para recomendar productos personalizados y aumentar tus ventas.',
      icon: '🤖',
      highlight: 'recommendations'
    },
    {
      title: 'Sistema de Afiliados',
      description: 'Gestiona tu programa de afiliados, rastrea comisiones y expande tu alcance con partners.',
      icon: '🤝',
      highlight: 'affiliates'
    },
    {
      title: '¡Todo Listo! ✨',
      description: 'Ya estás preparado para comenzar. Explora todas las funcionalidades y maximiza tu monetización.',
      icon: '🚀',
      highlight: null
    }
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    localStorage.setItem('onboarding_completed', 'true');
    setIsVisible(false);
    if (onComplete) onComplete();
  };

  const handleSkip = () => {
    localStorage.setItem('onboarding_completed', 'true');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  const step = steps[currentStep];
  const isLastStep = currentStep === steps.length - 1;
  const isFirstStep = currentStep === 0;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-60 transition-opacity"></div>

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full transform transition-all animate-scaleIn">
          {/* Close button */}
          <button
            onClick={handleSkip}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 z-10"
          >
            <X className="w-6 h-6" />
          </button>

          {/* Progress bar */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-700 rounded-t-2xl">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-tl-2xl transition-all duration-500"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            ></div>
          </div>

          {/* Content */}
          <div className="p-8 pt-12">
            {/* Icon */}
            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full text-5xl mb-4 animate-bounce">
                {step.icon}
              </div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
                {step.title}
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-300 max-w-xl mx-auto">
                {step.description}
              </p>
            </div>

            {/* Screenshot placeholder */}
            {step.highlight && (
              <div className="mt-8 rounded-xl overflow-hidden border-4 border-gray-200 dark:border-gray-700 shadow-xl">
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-700 dark:to-gray-800 h-64 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-6xl mb-4">{step.icon}</div>
                    <p className="text-gray-600 dark:text-gray-400 font-medium">
                      {step.highlight === 'dashboard' && 'Vista del Dashboard'}
                      {step.highlight === 'recommendations' && 'Sistema de Recomendaciones'}
                      {step.highlight === 'affiliates' && 'Panel de Afiliados'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Steps indicator */}
            <div className="flex justify-center gap-2 mt-8">
              {steps.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentStep(index)}
                  className={`h-2 rounded-full transition-all ${
                    index === currentStep
                      ? 'w-8 bg-blue-600'
                      : index < currentStep
                      ? 'w-2 bg-green-500'
                      : 'w-2 bg-gray-300 dark:bg-gray-600'
                  }`}
                ></button>
              ))}
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between mt-8">
              <button
                onClick={handlePrev}
                disabled={isFirstStep}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors ${
                  isFirstStep
                    ? 'text-gray-400 cursor-not-allowed'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <ChevronLeft className="w-5 h-5" />
                Anterior
              </button>

              <div className="text-sm text-gray-500 dark:text-gray-400">
                {currentStep + 1} de {steps.length}
              </div>

              <button
                onClick={handleNext}
                className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-all hover:scale-105"
              >
                {isLastStep ? (
                  <>
                    Comenzar
                    <Check className="w-5 h-5" />
                  </>
                ) : (
                  <>
                    Siguiente
                    <ChevronRight className="w-5 h-5" />
                  </>
                )}
              </button>
            </div>

            {/* Skip button */}
            {!isLastStep && (
              <div className="text-center mt-4">
                <button
                  onClick={handleSkip}
                  className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 underline"
                >
                  Saltar tutorial
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingFlow;

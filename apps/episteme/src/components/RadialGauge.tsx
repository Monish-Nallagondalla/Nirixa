'use client';

import React from 'react';

export type GaugeColor = 'tungsten' | 'emerald' | 'copper' | 'graphite';

interface RadialGaugeProps {
  value: number | string;
  max?: number;
  label: string;
  sublabel: string;
  color?: GaugeColor;
  icon?: React.ReactNode;
  size?: number; // diameter in px, default 84
  unit?: string;
  onClick?: () => void;
}

const colorMap = {
  tungsten: {
    stroke: '#C89B53',
    gradientId: 'radial-gauge-tungsten',
    gradientColors: ['#E5A93C', '#C89B53'],
    text: 'text-[#E5A93C]',
    bg: 'rgba(200, 155, 83, 0.08)'
  },
  emerald: {
    stroke: '#2E7D5B',
    gradientId: 'radial-gauge-emerald',
    gradientColors: ['#3EB67F', '#2E7D5B'],
    text: 'text-[#3EB67F]',
    bg: 'rgba(46, 125, 91, 0.08)'
  },
  copper: {
    stroke: '#B86B43',
    gradientId: 'radial-gauge-copper',
    gradientColors: ['#D97F52', '#B86B43'],
    text: 'text-[#D97F52]',
    bg: 'rgba(184, 107, 67, 0.08)'
  },
  graphite: {
    stroke: '#848C9E',
    gradientId: 'radial-gauge-graphite',
    gradientColors: ['#A6AEBF', '#848C9E'],
    text: 'text-[#A6AEBF]',
    bg: 'rgba(132, 140, 158, 0.08)'
  }
};

export default function RadialGauge({
  value,
  max = 100,
  label,
  sublabel,
  color = 'tungsten',
  icon,
  size = 84,
  unit = '',
  onClick
}: RadialGaugeProps) {
  const numericValue = typeof value === 'number' ? value : parseFloat(String(value).replace(/[^0-9.]/g, '')) || 0;
  const percentage = Math.min(Math.max((numericValue / max) * 100, 5), 100);

  const theme = colorMap[color] || colorMap.tungsten;

  // SVG Geometry
  const strokeWidth = 2.8;
  const radius = 18 - strokeWidth / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div
      onClick={onClick}
      className={`flex flex-col items-center text-center group select-none transition-all duration-200 ${
        onClick ? 'cursor-pointer hover:-translate-y-0.5' : 'cursor-default'
      }`}
      title={onClick ? `Click to inspect ${label}` : undefined}
    >
      <div
        className="relative flex items-center justify-center transition-transform duration-300"
        style={{ width: size, height: size }}
      >
        <svg
          className="w-full h-full transform -rotate-90"
          viewBox="0 0 36 36"
        >
          <defs>
            <linearGradient id={theme.gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={theme.gradientColors[0]} />
              <stop offset="100%" stopColor={theme.gradientColors[1]} />
            </linearGradient>
          </defs>

          {/* Background Track */}
          <circle
            cx="18"
            cy="18"
            r={radius}
            fill="none"
            stroke="rgba(255, 255, 255, 0.06)"
            strokeWidth={strokeWidth}
          />

          {/* Value Progress Ring */}
          <circle
            cx="18"
            cy="18"
            r={radius}
            fill="none"
            stroke={`url(#${theme.gradientId})`}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>

        {/* Center Metric Label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <div className="flex items-baseline">
            <span className="text-sm font-semibold tracking-tight text-[#EDEAE3] font-mono-precision">
              {value}
            </span>
            {unit && (
              <span className="text-[10px] text-[#9FA4B2] font-mono-precision ml-0.5">
                {unit}
              </span>
            )}
          </div>
          {icon && (
            <div className="mt-0.5 text-[#646979]">
              {icon}
            </div>
          )}
        </div>
      </div>

      {/* Primary & Sub-Labels */}
      <div className="mt-2 flex flex-col items-center">
        <span className="text-xs font-medium text-[#EDEAE3] tracking-tight group-hover:text-[#E5A93C] transition-colors">
          {label}
        </span>
        <span className="text-[10px] text-[#646979] font-mono-precision mt-0.5">
          {sublabel}
        </span>
      </div>
    </div>
  );
}

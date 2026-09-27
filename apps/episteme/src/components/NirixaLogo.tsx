'use client';

import React from 'react';

interface NirixaLogoProps {
  size?: number;
  showText?: boolean;
  version?: string;
}

export default function NirixaLogo({
  size = 36,
  showText = true,
  version = 'v1.1.0'
}: NirixaLogoProps) {
  return (
    <div className="flex items-center gap-3.5 select-none group cursor-pointer">
      {/* Precision Geometric Monogram 'N' + Epistemic Singularity Node */}
      <div
        className="relative flex items-center justify-center transition-all duration-300 group-hover:scale-105"
        style={{ width: size, height: size }}
      >
        <svg
          viewBox="0 0 44 44"
          className="w-full h-full"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="nirixa-left-stem" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#E5A93C" />
              <stop offset="100%" stopColor="#C89B53" />
            </linearGradient>

            <linearGradient id="nirixa-diagonal" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#E5A93C" />
              <stop offset="50%" stopColor="#C89B53" />
              <stop offset="100%" stopColor="#936A2A" />
            </linearGradient>

            <linearGradient id="nirixa-right-stem" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#C89B53" />
              <stop offset="100%" stopColor="#7E5618" />
            </linearGradient>

            <radialGradient id="singularity-glow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="1" />
              <stop offset="45%" stopColor="#E5A93C" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#C89B53" stopOpacity="0" />
            </radialGradient>
          </defs>

          {/* Background Ambient Charcoal Tile */}
          <rect
            x="2"
            y="2"
            width="40"
            height="40"
            rx="10"
            fill="#12151E"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="1"
          />

          {/* Left Vertical Pillar of 'N' */}
          <path
            d="M 12 11 L 17 11 L 17 33 L 12 33 Z"
            fill="url(#nirixa-left-stem)"
            stroke="rgba(229, 169, 60, 0.3)"
            strokeWidth="0.8"
          />

          {/* Dynamic Diagonal Bridge of 'N' */}
          <path
            d="M 12 11 L 19 11 L 32 33 L 25 33 Z"
            fill="url(#nirixa-diagonal)"
            stroke="rgba(200, 155, 83, 0.4)"
            strokeWidth="0.8"
          />

          {/* Right Vertical Pillar of 'N' */}
          <path
            d="M 27 11 L 32 11 L 32 33 L 27 33 Z"
            fill="url(#nirixa-right-stem)"
            stroke="rgba(147, 106, 42, 0.4)"
            strokeWidth="0.8"
          />

          {/* Central Singularity Node (Living Epistemic Spark at intersection) */}
          <circle cx="22" cy="22" r="3.5" fill="url(#singularity-glow)" />
          <circle cx="22" cy="22" r="1.5" fill="#ffffff" />
        </svg>
      </div>

      {/* Brand Typography */}
      {showText && (
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span className="text-base font-bold tracking-tight text-[#EDEAE3] font-editorial flex items-center">
              NIRIXA
              <span className="text-[#C89B53] font-mono-precision ml-1.5 font-medium text-xs tracking-wider">
                EPISTEME
              </span>
            </span>
            <span className="text-[10px] font-mono-precision px-1.5 py-0.5 rounded bg-[#C89B53]/10 border border-[#C89B53]/25 text-[#E5A93C] font-semibold tracking-wide">
              {version}
            </span>
          </div>
          <span className="text-[10px] font-mono-precision text-[#646979] tracking-wider uppercase">
            Cognitive Research OS
          </span>
        </div>
      )}
    </div>
  );
}

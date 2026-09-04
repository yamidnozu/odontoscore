import React, { useState } from 'react';

interface RadarChartProps {
  scores: {
    score_eficacia?: number;
    score_comodidad_encias?: number;
    score_durabilidad?: number;
    score_facilidad_uso?: number;
    score_silencio?: number;
    score_tecnologia?: number;
    score_calidad_precio?: number;
  };
  productName?: string;
  size?: number;
}

const AXES = [
  { key: 'score_eficacia', label: 'Eficacia' },
  { key: 'score_comodidad_encias', label: 'Encías' },
  { key: 'score_durabilidad', label: 'Durabilidad' },
  { key: 'score_facilidad_uso', label: 'Ergonomía' },
  { key: 'score_silencio', label: 'Silencio' },
  { key: 'score_tecnologia', label: 'Tecnología' },
  { key: 'score_calidad_precio', label: 'Calidad/Precio' }
];

export default function RadarChart({ scores, productName = '', size = 320 }: RadarChartProps) {
  const [hoveredAxis, setHoveredAxis] = useState<number | null>(null);

  const cx = size / 2;
  const cy = size / 2;
  const radius = (size / 2) * 0.72;
  const numAxes = AXES.length;

  const getCoordinates = (index: number, value: number) => {
    const angle = (Math.PI * 2 / numAxes) * index - Math.PI / 2;
    const r = (value / 10) * radius;
    return {
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle)
    };
  };

  // Build grid rings (2, 4, 6, 8, 10)
  const rings = [2, 4, 6, 8, 10];

  // Polygon points
  const points = AXES.map((axis, i) => {
    const rawVal = (scores as any)[axis.key] ?? 7.5;
    return getCoordinates(i, rawVal);
  });
  const polygonPointsStr = points.map(p => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

  return (
    <div className="radar-chart-container" style={{ position: 'relative', width: size, margin: '0 auto' }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="radar-svg" role="img" aria-label={`Gráfico radar clínico de ${productName}`}>
        {/* Background Grid Rings */}
        {rings.map(ringVal => {
          const ringPoints = AXES.map((_, i) => getCoordinates(i, ringVal));
          return (
            <polygon
              key={`ring-${ringVal}`}
              points={ringPoints.map(p => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')}
              fill="none"
              stroke="#e2e8f0"
              strokeWidth="1"
              strokeDasharray={ringVal === 10 ? 'none' : '2 2'}
            />
          );
        })}

        {/* Axis Lines */}
        {AXES.map((axis, i) => {
          const outer = getCoordinates(i, 10);
          return (
            <line
              key={`axis-line-${i}`}
              x1={cx}
              y1={cy}
              x2={outer.x}
              y2={outer.y}
              stroke="#cbd5e1"
              strokeWidth="1"
            />
          );
        })}

        {/* Data Polygon */}
        <polygon
          points={polygonPointsStr}
          fill="rgba(14, 118, 188, 0.22)"
          stroke="#0E76BC"
          strokeWidth="2.5"
          style={{ transition: 'all 0.3s ease' }}
        />

        {/* Data Points */}
        {points.map((p, i) => {
          const rawVal = (scores as any)[AXES[i].key] ?? 7.5;
          const isHovered = hoveredAxis === i;
          return (
            <g key={`point-${i}`} onMouseEnter={() => setHoveredAxis(i)} onMouseLeave={() => setHoveredAxis(null)} style={{ cursor: 'pointer' }}>
              <circle
                cx={p.x}
                cy={p.y}
                r={isHovered ? 6 : 4}
                fill="#0E76BC"
                stroke="#ffffff"
                strokeWidth="2"
              />
            </g>
          );
        })}

        {/* Axis Labels */}
        {AXES.map((axis, i) => {
          const labelCoord = getCoordinates(i, 11.8);
          const rawVal = (scores as any)[axis.key] ?? 7.5;
          const isHovered = hoveredAxis === i;
          return (
            <text
              key={`label-${i}`}
              x={labelCoord.x}
              y={labelCoord.y + 4}
              textAnchor="middle"
              fontSize={isHovered ? "11px" : "10px"}
              fontWeight={isHovered ? "800" : "600"}
              fill={isHovered ? "#0E76BC" : "#475569"}
              style={{ transition: 'all 0.2s ease', userSelect: 'none' }}
            >
              {axis.label} ({rawVal})
            </text>
          );
        })}
      </svg>
    </div>
  );
}

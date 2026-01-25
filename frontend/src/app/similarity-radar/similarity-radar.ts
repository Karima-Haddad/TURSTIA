import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-similarity-radar',
  imports: [CommonModule, MatIconModule],
  templateUrl: './similarity-radar.html',
  styleUrl: './similarity-radar.css',
})
export class SimilarityRadar implements OnChanges {

  @Input() radarPoints: any[] = [];

  hoveredPoint: any = null;

  CENTER_X = 200;
  CENTER_Y = 200;
  MAX_RADIUS = 150;

  positionedPoints: any[] = [];

  ngOnChanges() {
    if (this.radarPoints && this.radarPoints.length > 0) {
      this.positionedPoints = this.computeRadarPositions(this.radarPoints);
    }
  }

  computeRadarPositions(radarPoints: any[]) {

    const others = radarPoints.filter(p => p.type !== 'CURRENT');
    let i = 0;

    return radarPoints.map((p) => {

      // CURRENT toujours au centre
      if (p.type === 'CURRENT') {
        return {
          ...p,
          x: this.CENTER_X,
          y: this.CENTER_Y
        };
      }

      // Angle réparti uniformément
      const angle = i * (2 * Math.PI / others.length);
      i++;

      const score = p.score ?? 0;
      const radius = this.MAX_RADIUS * (1 - score);

      return {
        ...p,
        x: this.CENTER_X + radius * Math.cos(angle),
        y: this.CENTER_Y + radius * Math.sin(angle)
      };
    });
  }

  // Retourne la couleur en fonction du type de point
  getColor(p: any): string {
    if (p.type === 'CURRENT') return '#2ecc71'; // vert
    if (p.type === 'NORMAL')  return '#3498db'; // bleu
    if (p.type === 'FRAUD')   return '#e74c3c'; // rouge
    return '#95a5a6'; // gris
  }

  // Gestion du survol des points 
  onMouseEnter(point: any) {
  this.hoveredPoint = point;
  }

  onMouseLeave() {
    this.hoveredPoint = null;
  }


}

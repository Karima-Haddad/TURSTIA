import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-risk-factors-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './risk-factors-panel.html',
  styleUrls: ['./risk-factors-panel.css']
})
export class RiskFactorsPanel {
  @Input() riskFactors: string[] = [];
}

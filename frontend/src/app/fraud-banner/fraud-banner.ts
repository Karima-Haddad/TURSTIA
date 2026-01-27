import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FraudService } from '../services/fraud.service';

@Component({
  selector: 'app-fraud-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="fraudDetected" class="fraud-banner">
      🚨 Risque de fraude détecté pour le dossier {{ caseId }}
    </div>
  `,
  styles: [`
    .fraud-banner {
      background: #ffebee;
      color: #c62828;
      padding: 12px;
      border-radius: 6px;
      margin: 10px 0;
      font-weight: bold;
    }
  `]
})
export class FraudBannerComponent implements OnInit {

  // ✅ OBLIGATOIRE car utilisé depuis le parent
  @Input() caseId!: string;

  fraudDetected = false;

  constructor(private fraudService: FraudService) {}

  ngOnInit(): void {
    if (!this.caseId) {
      console.warn('⚠️ caseId non fourni à FraudBanner');
      return;
    }

    this.fraudService.getFraudStatus(this.caseId).subscribe({
      next: (res) => {
        this.fraudDetected = res.fraud_detected;
      },
      error: (err) => {
        console.error('Erreur API fraud_status', err);
      }
    });
  }
}
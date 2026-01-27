import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FraudService } from '../services/fraud.service';

@Component({
  selector: 'app-fraud-test',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Test liaison Front ↔ Back</h2>

    <div *ngIf="status">
      <p><b>Case ID :</b> {{ status.caseId }}</p>
      <p><b>Status :</b> {{ status.status }}</p>
      <p><b>Score :</b> {{ status.score }}</p>
      <p><b>Reason :</b> {{ status.reason }}</p>
      <p><b>Cold Start :</b> {{ status.cold_start }}</p>
    </div>
  `
})
export class FraudTestComponent implements OnInit {
  status: any;

  constructor(private fraudService: FraudService) {}

  ngOnInit() {
    this.fraudService.getFraudStatus('123').subscribe(res => {
      this.status = res;
    });
  }
}
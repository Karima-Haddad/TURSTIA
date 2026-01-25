import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { CommonModule } from '@angular/common'; 
import { ChangeDetectorRef } from '@angular/core';
import { SimilarityRadar } from '../similarity-radar/similarity-radar';

@Component({
  selector: 'app-demo',
  imports: [CommonModule,SimilarityRadar],
  templateUrl: './demo.html',
  styleUrl: './demo.css',
})
export class Demo {

  response = {
    mode: 'NORMAL',
    radar_points: [
      {
        type: 'CURRENT',
        case_id: 'NEW-1107',
        score: 1.0
      },
      {
        type: 'NORMAL',
        case_id: 'CASE-001',
        score: 0.85,
        decision: 'ACCEPT'
      },
      {
        type: 'NORMAL',
        case_id: 'CASE-002',
        score: 0.72,
        decision: 'ACCEPT_WITH_GUARANTEE'
      },
      {
        type: 'FRAUD',
        case_id: 'FRAUD-101',
        score: 0.41,
        fraud_type: 'identity'
      },
      {
        type: 'FRAUD',
        case_id: 'FRAUD-205',
        score: 0.33,
        fraud_type: 'document'
      }
    ]
  };

selectedCase = 'NORMAL';
  loading = false;
  result: any = null;

  constructor(private api: ApiService,
              private cdr: ChangeDetectorRef
  ) {}

  // ngOnInit(): void {
  //   this.runEvaluate();
  // }

  runEvaluate() {
    this.loading = true;
    this.result = null;

    this.api.evaluate({
      case_id: this.selectedCase
    }).subscribe({
      next: (res) => {
        console.log('API RESPONSE:', res);
        this.result = res;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('API ERROR:', err);
        this.loading = false;
      }
    });
  }
}

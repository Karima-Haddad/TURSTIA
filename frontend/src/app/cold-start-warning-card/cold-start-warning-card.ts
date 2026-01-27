
import { Component, Input, OnInit } from '@angular/core';
import { FraudService } from '../services/fraud.service';

@Component({
  selector: 'app-coldstart-warning',
  template: `
    <div *ngIf="coldStart" class="coldstart">
      ⚠️ Cold Start : Validation humaine requise
    </div>
  `
})
export class ColdStartWarningCardComponent implements OnInit {
  @Input() caseId: string = '';
  coldStart: boolean = false;

  constructor(private fraudService: FraudService) {}

  ngOnInit() {
    if (this.caseId) {
      this.fraudService.getFraudStatus(this.caseId).subscribe(res => {
        this.coldStart = res.cold_start;
      });
    }
  }
}
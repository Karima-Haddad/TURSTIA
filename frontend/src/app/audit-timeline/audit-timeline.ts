
import { Component, Input, OnInit } from '@angular/core';
import { FraudService } from '../services/fraud.service';


@Component({
  selector: 'app-audit-timeline',
  template: `
    <div *ngFor="let event of timeline">
      {{ event.timestamp }} - {{ event.message }}
    </div>
  `
})
export class AuditTimelineComponent implements OnInit {
  @Input() caseId: string = '';
  timeline: any[] = [];

  constructor(private fraudService: FraudService) {}

  ngOnInit() {
    if (this.caseId) {
      this.fraudService.getAuditTimeline(this.caseId).subscribe(res => {
        this.timeline = res.timeline;
      });
    }
  }
}
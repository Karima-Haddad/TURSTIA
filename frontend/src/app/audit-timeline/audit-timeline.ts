
import { Component, Input, OnInit } from '@angular/core';
import { FraudService } from '../services/fraud.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-audit-timeline',
  imports:[CommonModule],
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
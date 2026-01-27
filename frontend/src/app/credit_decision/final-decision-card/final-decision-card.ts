import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-final-decision-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './final-decision-card.html',
  styleUrls: ['./final-decision-card.css']
})
export class FinalDecisionCard {
  @Input() decision: any;
}

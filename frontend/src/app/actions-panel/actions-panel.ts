import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-actions-panel',
  standalone: true,
  templateUrl: './actions-panel.html'
})
export class ActionsPanel {

  @Output() evaluate = new EventEmitter<void>();
  @Output() feedback = new EventEmitter<void>();
}
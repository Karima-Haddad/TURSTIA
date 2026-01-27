import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-conditions-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './conditions-list.html',
  styleUrls: ['./conditions-list.css']
})
export class ConditionsList {
  @Input() conditions: string[] = [];
}

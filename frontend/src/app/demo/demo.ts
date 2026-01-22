import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { CommonModule } from '@angular/common'; 
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-demo',
  imports: [CommonModule],
  templateUrl: './demo.html',
  styleUrl: './demo.css',
})
export class Demo {

selectedCase = 'NORMAL';
  loading = false;
  result: any = null;

  constructor(private api: ApiService,
              private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.runEvaluate();
  }

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

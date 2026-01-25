import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Outcome } from './outcome';

describe('Outcome', () => {
  let component: Outcome;
  let fixture: ComponentFixture<Outcome>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Outcome]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Outcome);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

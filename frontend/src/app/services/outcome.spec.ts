import { TestBed } from '@angular/core/testing';

import { Outcome } from './outcome';

describe('Outcome', () => {
  let service: Outcome;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Outcome);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

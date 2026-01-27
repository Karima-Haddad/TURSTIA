import { TestBed } from '@angular/core/testing';

import { Evaluate } from './evaluate';

describe('Evaluate', () => {
  let service: Evaluate;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Evaluate);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

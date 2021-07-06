import { TestBed } from '@angular/core/testing';

import { BotMessageService } from './bot-message.service';

describe('BotMessageService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BotMessageService = TestBed.get(BotMessageService);
    expect(service).toBeTruthy();
  });
});

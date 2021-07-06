import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DiseaseInfoComponent } from './disease-info.component';

describe('DiseaseInfoComponent', () => {
  let component: DiseaseInfoComponent;
  let fixture: ComponentFixture<DiseaseInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DiseaseInfoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiseaseInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

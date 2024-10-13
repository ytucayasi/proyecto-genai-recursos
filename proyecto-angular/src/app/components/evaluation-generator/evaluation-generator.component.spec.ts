import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EvaluationGeneratorComponent } from './evaluation-generator.component';

describe('EvaluationGeneratorComponent', () => {
  let component: EvaluationGeneratorComponent;
  let fixture: ComponentFixture<EvaluationGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EvaluationGeneratorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EvaluationGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

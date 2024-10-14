import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { PresentationGeneratorComponent } from './presentation-generator.component';
import { of, throwError } from 'rxjs';

describe('PresentationGeneratorComponent', () => {
  let component: PresentationGeneratorComponent;
  let fixture: ComponentFixture<PresentationGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormsModule, PresentationGeneratorComponent]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PresentationGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should generate presentation on form submit', () => {
    const mockResult = { pptx: 'mockPptxUrl', pdf: 'mockPdfUrl' };
    spyOn(component, 'generatePresentation').and.returnValue(of(mockResult));

    component.request = { msg: 'Test Presentation', design: 1, slides: 10 };
    component.onSubmit();

    expect(component.generatePresentation).toHaveBeenCalledWith(component.request);
    expect(component.result).toEqual(mockResult);
    expect(component.isLoading).toBeFalse();
    expect(component.errorMessage).toBeNull();
  });

  it('should handle errors when generating presentation', () => {
    spyOn(component, 'generatePresentation').and.returnValue(throwError('Test error'));

    component.request = { msg: 'Test Presentation', design: 1, slides: 10 };
    component.onSubmit();

    expect(component.generatePresentation).toHaveBeenCalledWith(component.request);
    expect(component.result).toBeNull();
    expect(component.isLoading).toBeFalse();
    expect(component.errorMessage).toBe('Ocurrió un error al generar la presentación. Por favor, intenta de nuevo.');
  });
});
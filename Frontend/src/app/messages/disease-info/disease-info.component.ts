import { Component, Input, OnInit } from '@angular/core';
import { faAmbulance, faCheck, faHospital, faPlus, faPlusCircle, faSyringe } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-disease-info',
  templateUrl: './disease-info.component.html',
  styleUrls: ['./disease-info.component.scss']
})
export class DiseaseInfoComponent implements OnInit {
  @Input() diseaseInfo;
  displayEle ="overview";
  faSyringe = faSyringe;
  faPlus = faPlusCircle;
  faAmbulance = faAmbulance;
  faCheck = faCheck;
  faHospital = faHospital;
  showFullOver = false;
  constructor() { }

  ngOnInit() {
  }

}

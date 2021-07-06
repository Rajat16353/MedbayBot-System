import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { BotMessageService } from '../bot-message.service';

@Component({
  selector: 'app-symptoms',
  templateUrl: './symptoms.component.html',
  styleUrls: ['./symptoms.component.scss']
})
export class SymptomsComponent implements OnInit {
  @Input() symptoms : any;
  @Input() hasSkipList: boolean;
  skipList= new Set<string>();
  i=0;
  maxVisited = 0;
  displaySize = 5;
  displaySymptoms : any;
  selectedSymptomsSet= new Set<string>();
  bgColorOnclick = 'rgb(0, 123, 255)' ;
  bgColorOnHover = 'rgb(86, 171, 255)' ;
  defaultBgColor = 'white';
  constructor(private botMessageService:BotMessageService,
              private apiService:ApiService) { }

  ngOnInit() {

    if(!this.hasSkipList) {
      this.displaySymptoms = this.symptoms;
    } else {
      this.displaySymptoms = this.symptoms.slice(this.i,Math.min(this.i+this.displaySize,this.symptoms.length));
      this.i +=this.displaySize;
      this.maxVisited = this.i;
    }
  }
  changeBgToBlue(event) {
    //console.log('current color'+event.target.style.backgroundColor);
    if(event.target.style.backgroundColor !== this.bgColorOnclick){
      event.target.style.backgroundColor = event.type === "mouseenter" ? this.bgColorOnHover : this.defaultBgColor ;
    }
  }
  symptomClicked(symptom:string,event) {
    //console.log(symptom +' added')
     if(event.target.style.backgroundColor === this.bgColorOnclick){
      event.target.style.backgroundColor =  this.defaultBgColor ;
      this.selectedSymptomsSet.delete(symptom);
    } else {
      this.selectedSymptomsSet.add(symptom);
      event.target.style.backgroundColor =  this.bgColorOnclick ;
    } 
    this.botMessageService.allSelectedSymptoms.add(symptom);
   /*  if(!this.selectedSymptomsSet.has(symptom)) {
      this.selectedSymptomsSet.add(symptom);
    } else {
      this.selectedSymptomsSet.delete(symptom);
    } */
  }
  createSkipList(predict:boolean) {
    let j;
    for(j=0;j<this.maxVisited;j++){
        if(!this.selectedSymptomsSet.has(this.symptoms[j])){
          this.botMessageService.allSkippedSymptoms.add(this.symptoms[j]);
        } else {
          this.botMessageService.allSelectedSymptoms.add(this.symptoms[j]);
        }
    }
    if(j == this.maxVisited) {
      console.log("skiplist "+JSON.stringify(this.skipList));
      this.sendFinalSymptoms(predict);
    }
  }
  sendFinalSymptoms(predict:boolean) {
    this.botMessageService.botTypingListener.next(true);
    var messageForBot = {
      "name":'a',
      "age":'20',
      "gender":'male',
      "found_symptoms": null,
      "text":Array.from(this.botMessageService.allSelectedSymptoms),
      "skip_symptoms":Array.from(this.botMessageService.allSkippedSymptoms),
      "predict":predict
    }
    this.botMessageService.messages.push({message:'I am experiencing : '+Array.from(this.selectedSymptomsSet).join(" "),symptoms:[],owner:'user'})
    this.apiService.sendMessage(messageForBot).subscribe((res)=>{
        this.botMessageService.generateBotMessage(res);
      });
  }

  showPrev(){
    if(this.i>0){
      this.i -=this.displaySize;
    }
    this.displaySymptoms = this.symptoms.slice(this.i,this.i+this.displaySize)
  }

  showNext(){
    this.displaySymptoms = this.symptoms.slice(this.i,Math.min(this.i+this.displaySize,this.symptoms.length));
   if(this.i + this.displaySize < this.symptoms.length) {
    this.i +=this.displaySize;
    this.maxVisited = this.i;
   }
  }

}

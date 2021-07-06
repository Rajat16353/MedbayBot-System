import { Injectable } from '@angular/core';
import { faSleigh } from '@fortawesome/free-solid-svg-icons';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BotMessageService {
  messagesChanged = new Subject<any[]>();
  startForCooccuringList=0;
  botTypingListener = new Subject<boolean>();
  username:string = null;
  age: number = null;
  gender: string = null;
  allSelectedSymptoms = new Set<any>();
  allSkippedSymptoms = new Set<any>();
  drugInfo = false;
  messages= [
    /*  {message:"n publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without",owner:'user'},
     {message:"n publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without",owner:'user'},
     {message:"n publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without",owner:'bot'},
     {message:"n publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without",owner:'user'},
     {message:"Are you experiencing any of the following ?",symptoms:["Fever" ,"Headache" ,"Coughing"],owner:'bot'} */
   ]
  constructor() { }
  generateBotMessage(res){
    var msg;

    console.log('response '+JSON.stringify(res));
    if(res.drug_info_flag) {
      this.drugInfo = res.drug_info_flag;
    }
    if(!this.username && res.name) {
      this.username = res.name;
    }
    if(!this.age && res.age) {
      this.age = res.age;
    }
    if(!this.gender && res.gender) {
      this.gender = res.gender;
    }
    if(Array.isArray(res.response) ) { // string of messages
      res.response.forEach((text) => {
        msg = {
          message:text,
          symptoms:[],
          owner:'bot'}
          this.sendBotMessage(msg);
      });
    } else { //single message
      msg = {
        message:res.response,
        symptoms:[],
        owner:'bot'}
        this.sendBotMessage(msg);
    }
    this.messagesChanged.next(this.messages);
        if(res.gender_query && !this.gender) {
          msg = {
            genderQuery : res.gender_query,
            owner : 'bot'}
          this.sendBotMessage(msg);
        }
        if(res.found_symptoms && res.found_symptoms.length>0){
          msg = {
            symptoms:res.found_symptoms,
            owner:'bot'}
            this.sendBotMessage(msg);
        } else if (res.co_occuring){
          let symptomsList= this.getCoocurringSymptoms(res.co_occuring);
          msg = {
            finalSymptoms:symptomsList,
            owner:'bot'}
            this.sendBotMessage(msg);
        } else if(res.diseases_list) {
          msg = {
            message:'Based on the data provided you may have : ',
            diseaseList:res.diseases_list,
            owner:'bot'}
            this.sendBotMessage(msg);
        } else if(res.drug_list) {
          console.log("in here 1");
          if(res.drug_list.drug_list.length > 0  ) {
            console.log("in here 2");
            msg = {
              message:'Please select the most relevant drug from below : ',
              drugList:res.drug_list,
              owner:'bot'}
          } else {
            console.log("in here 3");
            msg = {
              message:'I found this info regarding your query ',
              drugList:res.drug_list,
              owner:'bot'}
          }
          
            this.sendBotMessage(msg);
        }
          
  }
  generateDiseaseInfo(res){
    console.log(res);
    let msg = res;
    this.sendBotMessage(msg);

  }
  sendBotMessage(msg) {
    this.botTypingListener.next(true);
    setTimeout(()=>{
     // console.log("msg is "+JSON.stringify(msg));
      this.messages.push(msg);
      this.botTypingListener.next(false);
      this.messagesChanged.next(this.messages);
    },3000)
  }
  getCoocurringSymptoms(res) {
    this.startForCooccuringList =0;
    console.log('res before symptoms list '+JSON.stringify(res));
    let symptomsList = [];
    do{
      symptomsList.push(res[this.startForCooccuringList].symptom);
      this.startForCooccuringList++;
      console.log('start for coocurring'+this.startForCooccuringList);
    }while(this.startForCooccuringList<res.length)
    console.log('symptoms list '+JSON.stringify(symptomsList));
    return symptomsList;
  }
  getDiseases(disease_list){
    var diseases = [];
    for(let i=0;i<disease_list.length;i++) {
      diseases.push(disease_list[i].Disease_name)
    }
    return diseases.toString();
  }
}

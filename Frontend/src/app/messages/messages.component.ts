import { ThrowStmt } from '@angular/compiler';
import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { ApiService } from '../api.service';
import { BotMessageService } from '../bot-message.service';
import { DrugInfoComponent } from './drug-info/drug-info.component';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.scss']
})
export class MessagesComponent implements OnInit {
  @ViewChild('drugList',{static:false}) drugList: DrugInfoComponent;
  selectedSymptomsSet= new Set<string>();

  cooccuringSymptomsSet = new Set<string>();
  bgClass ="";
  returnMsg :any;
  messages = [];
  botTyping = false;
  gender ="";
  constructor(private apiService:ApiService ,private changeDetector:ChangeDetectorRef,private botMessageService:BotMessageService) { }
  ngOnInit() {
    this.messages = this.botMessageService.messages;
    let chatBox :HTMLElement= document.getElementById('message-component');
    chatBox.scrollTop = chatBox.scrollHeight;
    this.botMessageService.messagesChanged.subscribe((res)=>{
      this.messages = res;
      this.changeDetector.detectChanges();
      let chatBox :HTMLElement= document.getElementById('message-component');
      chatBox.scrollTop = chatBox.scrollHeight;
      let chatBox1 :HTMLElement= document.getElementById('chat-box');
      chatBox1.scrollTop = chatBox1.scrollHeight;
    })
    this.botMessageService.botTypingListener.subscribe((res) =>{
      if(res) {
        this.botTyping = true;
      } else {
        this.botTyping =false;
      }
    })


     /*this.apiService.getDiseaseInfo({
      "disease_name":"Coronavirus"
    }).subscribe((res)=>{
      this.botMessageService.generateDiseaseInfo(res);
    }) */

    ///drugs/crocin-advance-tablet-600468
    /* let messageForBot = {
      "name":this.botMessageService.username,
      "age":this.botMessageService.age,
      "gender":this.botMessageService.gender,
      "text":"",
      "selected_drug_link":"/drugs/crocin-advance-tablet-600468"
    }
    this.botMessageService.messages.push({message:name,symptoms:[],owner:'user'})
      this.botMessageService.messagesChanged.next(this.botMessageService.messages);
      this.apiService.sendMessage(messageForBot).subscribe((res)=>{
        this.botMessageService.generateBotMessage(res);
      }); */
  }

  setGender(value:string) {
      this.gender = value;
      this.botMessageService.messages.push({message:"I am a "+this.gender,symptoms:[],owner:'user'})
      this.sendGender();
  }
  sendGender() {
    this.apiService.sendMessage({
    "name":this.botMessageService.username,
    "age":this.botMessageService.age,
    "gender":this.botMessageService.gender,
    "text":this.gender}).subscribe((res)=>{
      this.botMessageService.generateBotMessage(res);
    });
  }

  getDiseaseInfo(name:string){
    this.apiService.getDiseaseInfo({
      "disease_name":name
    }).subscribe((res)=>{
      this.botMessageService.generateDiseaseInfo(res);
    })
  }
  
  
  
}

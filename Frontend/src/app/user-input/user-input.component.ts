import { ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { faArrowAltCircleRight, faCoffee, faMicrophone, faSmile } from '@fortawesome/free-solid-svg-icons';
import { ApiService } from '../api.service';
import { BotMessageService } from '../bot-message.service';

@Component({
  selector: 'app-user-input',
  templateUrl: './user-input.component.html',
  styleUrls: ['./user-input.component.scss']
})
export class UserInputComponent implements OnInit {
  @ViewChild('textInput',{static:false}) textInput: ElementRef;
  faEmoji = faSmile;
  faSend = faArrowAltCircleRight;
  faMic = faMicrophone;
  constructor(private apiService:ApiService,
     private botMessageService:BotMessageService ) { }

  ngOnInit() {
    let messageForBot = {
      "name":this.botMessageService.username,
      "age":this.botMessageService.age,
      "gender":this.botMessageService.gender,
      "text":""
    }
    this.apiService.sendMessage(messageForBot).subscribe((res)=>{
      this.botMessageService.generateBotMessage(res);
    });
  }

  sendUserMessage(text:string){
    this.botMessageService.botTypingListener.next(true);
      var messageForBot 
      if(this.botMessageService.drugInfo) {
        console.log("sending drug name");
        messageForBot = {
          "name":this.botMessageService.username,
          "age":this.botMessageService.age,
          "gender":this.botMessageService.gender,
          "text":"",
          "drug_name":text
        }
      } else {
        messageForBot = {
          "name":this.botMessageService.username,
          "age":this.botMessageService.age,
          "gender":this.botMessageService.gender,
          "text":text,
        }
      }
      this.botMessageService.messages.push({message:text,symptoms:[],owner:'user'})
      this.botMessageService.messagesChanged.next(this.botMessageService.messages);
      this.textInput.nativeElement.value = '';
      this.apiService.sendMessage(messageForBot).subscribe((res)=>{
        this.botMessageService.generateBotMessage(res);
      });
  }

}

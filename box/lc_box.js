// 20210504,20231012
Date.prototype.format_old = function(s) {               // date format YYYY-MM-DD hh:mm:ss.fff local timezone
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();
  var hh = this.getHours();
  var mi = this.getMinutes();
  var ss = this.getSeconds();
  var ff = this.getMilliseconds();
  var zz = this.getTimezoneOffset();
  var z1 = Math.abs(zz);
  var f  = [this.getFullYear()
    	, '-', (mm>9 ? '' : '0') + mm
      , '-', (dd>9 ? '' : '0') + dd
      , ' ', (hh>9 ? '' : '0') + hh
      , ':', (mi>9 ? '' : '0') + mi
      , ':', (ss>9 ? '' : '0') + ss
      , '.', ff.toString().padStart(3,'0')
      , (zz>=0 ? '-' : '+')
      , Math.floor(z1/60).toString().padStart(2,'0')
      , (z1%60).toString().padStart(2,'0')
		].join('');
    return f;
    };
// document.write('<p>'+new Date().format_old());
// document.write('<p>'+new Date().toISOString());  // UTC, not local time

function unit_test_only(item=02) {
  if (item==1){
    console.log(new Date()+':'+'test')
    console.log(Intl.DateTimeFormat().resolvedOptions().timeZone)
    console.log(new Date().getTimezoneOffset())
  }
  if (item==2) {
    console.log(new Date().format_old())   // 2023-10-12 23:29:47.742+0800
  }
}

// LC toolbox (20221105..1130..1204): class LC_latex, LC_prompt, Date.prototype.format, LC_login
class LC_latex {
	constructor() {
		}
	html(v_str,v_dlm='$$') {// return html with img on latex
		let j=0, v_result='';
		for (let i=0;i<v_str.length;i++) {
			let chk=this.pos_around(v_str,j);
			if (chk[1]==-1) {v_result+=v_str.substr(j);}
			else {v_result+=v_str.substr(j,chk[0]-j)+this.img_latex(v_str.substr(chk[0],chk[1]-chk[0]+1));}
			if (chk[1]>=0) {j=chk[1]+1;} else {break;}
			}
		return v_result;
		} //html
	html2(v_str,v_dlm='$$') {// return html with img on latex or simply img on latex if prefix by '$$'
		if (v_str.substr(0,v_dlm.length)==v_dlm) return this.img_latex(v_str.substr(v_dlm.length),v_dlm);
		else {
		let j=0, v_result='';
		for (let i=0;i<v_str.length;i++) {
			let chk=this.pos_around(v_str,j);
			if (chk[1]==-1) {v_result+=v_str.substr(j);}
			else {v_result+=v_str.substr(j,chk[0]-j)+this.img_latex(v_str.substr(chk[0],chk[1]-chk[0]+1));}
			if (chk[1]>=0) {j=chk[1]+1;} else {break;}
			}
		return v_result;
		}
		} //html2
	pos_around(v_str,v_start=0,v_dlm='$$') {
		let d=v_dlm.length, x=v_str.indexOf(v_dlm,v_start), y=(x>=0)?v_str.indexOf(v_dlm,x+d):-1;
		return [x,(y>=0)?y+d-1:-1,(y>=0)?v_str.substr(x,y+d-x):null,v_str,v_start,v_dlm];
		}
	html_decode(v_str) {return v_str.replace(/&gt;/g,'>').replace(/&lt;/g,'<')}
	img_latex(v_str) {
		let n=v_str.length;
		if (n<4) return v_str;
		if (v_str.substr(0,2)!='$$' || v_str.substr(n-2,2)!='$$') return v_str;
		let v_latex =encodeURIComponent(this.html_decode(v_str.substr(2,n-4)));
		return '<img class="IMG_LATEX" data-latex="#s_latex#" src="https://i.upmath.me/svg/#v_latex#" style="max-width:80%"></img>'.replace(/#v_latex#/g,v_latex).replace(/#s_latex#/g,v_str.substr(2,n-4));
		}
	img_src(v_str) {
		if (v_str.substr(0,8)=='exercise') return 	'https://raw.githubusercontent.com/leo202103/public_area/main/img/'+v_str;
		return 'https://i.upmath.me/svg/'+encodeURIComponent(this.html_decode(v_str));
		}
	} //class LC_latex
class LC_prompt {
	constructor() {
		}
	messageBox(msg='System Message ...') {
		let w=300;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2a=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message ...
		$(div0).addClass('w3-modal');
		$(div1).addClass('w3-modal-content w3-display-container');
		$(div1a).addClass('w3-card');
		$(div2).height(40).css('min-width',w).addClass('w3-display-topmiddle w3-center w3-blue').text('Message').css('padding-top','8px').css('margin','0');
		$(div2a).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-center w3-white').text(msg)
			.css('margin-top','15px').css('padding-top','30px').css('min-width',w).css('min-height',100);
		div0.appendChild(div1);
		div1.appendChild(div1a);
		div1a.appendChild(div2).appendChild(div3);
		div2.appendChild(div2a);
		document.body.appendChild(div0);
		$(div0).show();
		} //messageBox
	inputBox(msg='Input:', f_ok=(v_input)=>{}, v_init=null, v_list=null, v_attr={}) {
		let w=400, h=100;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2a=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message ...
		let input0 =document.createElement('input'); //input box
		let btn0 =document.createElement('button');     //ok button
		$(div0).addClass('w3-modal').append(div1);
		$(div1).addClass('w3-modal-content w3-display-container').append(div1a).append(div2);
		$(div1a).addClass('w3-card');
		$(div2).height(40).width(w).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Input Box').css('padding-top','8px').css('margin','0')
			.append(div2a).append(div3);
		$(div2a).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-center w3-white').text(msg)
			.css('margin-top','15px').css('padding-top','20px')
			.css('min-width',w).css('min-height',h)
			.append(input0).append(btn0);
		$(input0).addClass('w3-text-black').css('margin','20px').val(v_init);
		$(btn0).text('OK').css('margin',5).click((e)=>{
			f_ok($(e.target).parents('.w3-modal').find('input').val());
			$(e.target).parents('.w3-modal').remove();
			});
		if (v_list!=null) {
			let unique_id0=this.unique_id('list');
			let list0 =document.createElement('datalist');  //input selection list
			$(input0).attr('list',unique_id0);
			$(list0).attr('id',unique_id0);
			for (let v of v_list) {$(list0).append('<option>'+v+'</option>');}
			$(div0).append(list0);
			// disable datalist filter by following
			$(input0).on('click', function() {
				$(this).data('previousValue',$(this).val());
				$(this).val('');
				});
			$(input0).on('mouseleave', function() {
				if ($(this).val() == '') {$(this).val($(this).data('previousValue'));}
				});
			}
		for (let k of Object.keys(v_attr)) {$(input0).attr(k, v_attr[k]);} //Object.keys(v_attr).length>0
		$(document.body).append(div0);
		$(div0).show();
		$(input0).focus();
		} //inputBox

	selectBox(msg='Select:', f_ok=(v_input)=>{}, v_list=null, v_init=null, v_size=null) {
		let w=400, sel_i=-1;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2a=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message ...
		let select0 =document.createElement('select');    //input box
		let btn0 =document.createElement('button');     //ok button
		let list0 =document.createElement('options');  //input selection list
		$(div0).addClass('w3-modal').append(div1).append(list0);
		$(div1).addClass('w3-modal-content w3-display-container').append(div1a).append(div2);
		$(div1a).addClass('w3-card');
		$(div2).height(40).width(w).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Select Box').css('padding-top','8px').css('margin','0')
			.append(div2a).append(div3);
		$(div2a).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-center w3-white').text(msg)
			.css('margin-top','15px').css('padding-top','20px').width(w).css('min-height',100)
			.append(select0).append(btn0);
		$(select0 ).addClass('w3-text-black').css('margin','20px').css('min-width','50px');
		$(btn0).text('OK').click((e)=>{
			f_ok($(e.target).parents('.w3-modal').find('select').val());
			$(e.target).parents('.w3-modal').remove();
			});
		for (let i in v_list) {let opt0=document.createElement('option');
			opt0.text=v_list[i]; select0.options.add(opt0);
			if (v_list[i]==v_init) {sel_i=i;}
			}
		select0.selectedIndex=sel_i;
		if (v_size>1) {$(select0).before('<br>');select0.size=v_size;$(select0).after('<br>');}
		$(document.body).append(div0);
		$(div0).show();
		} //selectBox
	textBox(msg='Input text:', f_ok=(v_input)=>{}, v_init=null, v_json='N', v_param={}) {
		let w=400, h=100;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2a=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message ...
		let textarea0=document.createElement('textarea');    //textpad box
		let btn0 =document.createElement('button');     //ok button
		$(div0).addClass('w3-modal').append(div1);
		$(div1).addClass('w3-modal-content w3-display-container w3-yellow')
			.append(div1a).append(div2);
		$(div1a).addClass('w3-card');
		$(div2).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Text Box').css('padding-top','8px').css('margin','0')
			.append(div2a).append(div3);
		$(div2a).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-center w3-white').text(msg)
			.css('margin-top','15px').css('padding-top','20px')
			.append(textarea0).append(btn0);
		$(textarea0).addClass('w3-text-black').css('margin','20px')
			.css('height',h).css('width',w).val(v_init);
		if (v_param.readOnly) {$(textarea0).attr('readOnly',true);}
		$(btn0).text('OK').css('margin',10).click((e)=>{
			let v=$(e.target).parents('.w3-modal').find('textarea').val(), v1=null;
			if (v_json=='Y') {v1=this.parse_json(v);
				if (typeof v1=='string') {alert('JSON ERR:'+v1); return;}
				}
			if (v_json=='Y') {f_ok(v1);} else {f_ok(v);}
			$(e.target).parents('.w3-modal').remove();
			});
		$(document.body).append(div0);
		$(div0).show();
		} //textBox
	mathsBox(msg='Edit formula using LaTex script:', f_ok=(v_input)=>{}, v_init=null, v_json='N') {
		let w=400, h=100, i, x;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2a=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message ...
		let div3a=document.createElement('div'); //symbol library btn
		let div3b=document.createElement('div'); //symbol library
		let div4 =document.createElement('div'); //bottom buttons (OK)
		let label0 =document.createElement('label');
		let textarea0=document.createElement('textarea');    //textpad box
		let img0=document.createElement('img');    //textpad box
		let btn0 =document.createElement('button');     //ok button
		$(div0).addClass('w3-modal').append(div1);
		$(div1).addClass('w3-modal-content w3-display-container').append(div1a).append(div2);
		$(div1a).addClass('w3-card');
		$(div2).height(40).css('min-width',w).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Formula Box').css('padding-top','8px').css('margin','0')
			.append(div2a).append(div3).append(div4);
		$(div2a).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-center w3-white w3-tiny')
			.css('margin-top','12px').css('padding-top','10px').css('min-width',w).css('min-height',h)
			.append(label0).append(div3a).append(div3b).append(textarea0).append('<br>').append(img0);
		$(div3a).addClass('w3-right w3-btn w3-tiny').text('symbol library')
			.css('margin','2px').css('padding','2px').click((e)=>{
				$(e.target).parents('div').find('div.LC_formula').toggle();
				});
		$(div3b).addClass('w3-green LC_formula').width('90%')
			.css('overflow','auto').css('height','150px').css('margin','5%')
			.css('text-align','left').hide();
		let latex_list =[['{x^2}','{x^n}','{x\\over y}','{x_m}','{x_m^n}','{x^\\circ}','{\\sqrt{x}}','{\\sqrt[n]{x}}']
			, ['\\pi','\\theta','\\alpha','\\beta','\\gamma','\\delta','\\epsilon','\\varepsilon','\\zeta','\\eta'
				,'\\theta','\\vartheta','\\iota','\\kappa','\\varkappa','\\lambda','\\mu','\\nu','\\xi','\\varpi','\\rho'
				,'\\varrho','\\sigma','\\varsigma','\\tau','\\upsilon','\\phi','\\varphi','\\chi','\\psi','\\omega']
			, ['\\Gamma','\\Delta','\\Theta','\\Lambda','\\Xi','\\Pi','\\Sigma','\\Upsilon','\\Phi','\\Psi','\\Omega']
			, ['\\leq','\\geq','\\neq','\\equiv','\\pm','\\infty','\\therefore','\\because','\\ll','\\subset','\\subseteq'
				,'\\nsubseteq','\\sqsubset','\\sqsubseteq','\\preceq','\\gg','\\supset','\\supseteq','\\nsupseteq','\\sqsupset','\\sqsupseteq','\\succeq']
			, ['\\sum','{\\text{d}\\over \\text{d}x}','\\int', '\\,\\mathrm{d}x','\\sum_{i=1}^{n} x_i','\\int_a^b y\\,\\mathrm{d}x','\\prod'
				,'\\oint','\\iint','\\iiint','\\iiiint','\\idotsint']
			, ['\\sin','\\cos','\\tan','\\cot','\\sec','\\csc','\\arcsin','\\arccos','\\arctan','\\sinh','\\cosh','\\tanh','\\coth']
			, ['\\pm','\\mp','\\times','\\div','\\ast','\\star','\\dagger','\\ddagger','\\cap','\\cup','\\uplus','\\sqcap','\\sqcup','\\vee','\\wedge','\\cdot']
			, ['\\left(..\\right)','\\left\\{..\\right\\}','\\big(','\\Big(','\\bigg(','\\Bigg(','\\big)','\\Big)','\\bigg)','\\Bigg)']
			, ['\\partial','\\eth','\\hbar','\\imath','\\jmath','\\ell','\\Re','\\Im','\\wp','\\nabla','\\Box','\\infty','\\aleph','\\beth','\\gimel']
			, ['\\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}','\\begin{bmatrix} 1 & 2 \\\\ 3 & 4 \\end{bmatrix}','\\begin{matrix} 1 & 2 \\\\ 3 & 4 \\end{matrix}','\\left(\\begin{smallmatrix} 1&2 \\\\ 3&4 \\end{smallmatrix} \\right)']
			, ['\\angle','\\emptyset','\\forall','\\in','\\notin','\\exists','\\nexists','\\neg','\\subset','\\supset','\\notin','\\ni','\\land','\\lor','\\rightarrow','\\leftarrow'
				,'\\mapsto','\\implies','\\impliedby','\\Rightarrow','\\leftrightarrow','\\iff','\\Leftrightarrow','\\top','\\bot','\\varnothing','\\rightleftharpoons']
			, ['\\|','\\{','\\}','\\mid','\\uparrow','\\downarrow','\\Uparrow','\\Downarrow','\\langle','\\lceil','\\lfloor','\\backslash','\\rangle','\\rceil','\\rfloor','\\ulcorner','\\urcorner']
			, ['\\doteq','\\equiv','\\approx','\\cong','\\simeq','\\sim','\\propto','\\neq','\\asymp','\\vdash','\\in','\\smile','\\models','\\perp','\\prec','\\sphericalangle','\\nparallel'
				,'\\bowtie','\\dashv','\\ni','\\frown','\\notin','\\succ','\\measuredangle']
			, ['\\bigoplus','\\bigcup','\\bigsqcup','\\bigotimes','\\bigcap','\\bigvee','\\coprod','\\bigodot','\\biguplus','\\bigwedge']
			, ['\\left.\\right|_a^b','\\bmod n', '\\pmod{n}','\\dots','\\ldots','\\cdots','\\ddots']
			, ['\\overrightarrow{AB}','\\overline{aaa}a^','\\prime','\\hat{a}','\\grave{a}','\\dot{a}','\\not{a}','\\dddot{a}','\\widehat{AAA}','\\stackrel\\frown{AAA}','\\tilde{a}'
				,'\\overleftarrow{AB}','\\widetilde{AAA}','\\bar{a}','\\acute{a}','\\ddot{a}','\\mathring{a}','\\check{a}','\\vec{a}','\\ddddot{a}','\\underline{a}']
			];
		let div6 =document.createElement('div'); //{} buttons
		$(div6).addClass("w3-button w3-padding-small").attr('title',"round marked text by {}").attr('data-latex','{}').text('{}')
			.click((e)=>{this.insert_txt(e);});
		$(div3b).append(div6);
		for (x of latex_list) { // add latex to symbol library
			for (i=0;i<x.length;i++) {
				let img1=document.createElement('img');
				$(img1).addClass('w3-button w3-padding-small')
				.attr('data-latex',x[i])
				.attr('src','https://i.upmath.me/svg/#v_latex#'.replace('#v_latex#',encodeURIComponent(x[i])))
				.click((e)=>{this.insert_txt(e);}); //insert symbol to textarea
				$(img1).addClass((i>=3)?'LC_more':'LC_show')
				$(div3b).append(img1);
				}
			if (x.length>3) { // add btn to show/hide more items
				let div5 =document.createElement('div');
				$(div5).addClass("w3-button w3-padding-small w3-tiny w3-text-gray").text('...')
					.click((e)=>{
						let s0=($(e.target).text()=='...')?'<<':'...';
						$(e.target).text(s0).prevUntil('img.LC_show').toggle();
						});
				$(div3b).append(div5);
				}
			$(div3b).find('img.LC_more').hide();
			}
		$(div4).addClass('w3-center w3-white').append(btn0);
		$(textarea0).addClass('w3-text-black').css('margin','20px').width('90%').val(v_init)
			.attr('placeholder','edit formula using LaTex')
			.css('margin','0px').css('padding','2px')
			.on('input',(e)=>{
			e.cancelBubble = true;
			let v=$(e.target).parents('.w3-modal').find('img.LC_preview'), v1=$(e.target).val();
			$(v).attr('src','https://i.upmath.me/svg/#v_latex#'.replace('#v_latex#',encodeURIComponent(v1)));
			});
		$(img0).attr('src','https://i.upmath.me/svg/y%3Df(x)').addClass('w3-row')
			.addClass('LC_preview').attr('title','formula preview');
		$(btn0).text('OK').css('margin',10).addClass('w3-row').click((e)=>{
			let v=$(e.target).parents('.w3-modal').find('textarea').val(), v1=null;
			if (v_json=='Y') {v1=this.parse_json(v);
				if (typeof v1=='string') {alert('JSON ERR:'+v1); return;}
				}
			if (v_json=='Y') {f_ok(v1);} else {f_ok(v);}
			$(e.target).parents('.w3-modal').remove();
			});
		$(label0).addClass('w3-left').text(msg).css('padding-left','5px');
		$(document.body).append(div0);
		$(div0).show();
		$(textarea0).trigger('input');
		$(textarea0).focus();
		} //mathsBox
	unique_id(prefix='id') {
		for (let i=0;i<9999;i++) {
		if ($('#'+prefix+i).attr('id')==undefined) {return prefix+i;}
		}}
	parse_json(v) {
		try {return JSON.parse(v);}
		catch(err) {return err.message;}
		}
	insert_txt(e) {  // insert string s into textarea under the selection (markted text)
		let obj_text=$(e.target).parents('.w3-modal').find('textarea')[0], s=$(e.target).attr('data-latex');
		let s0=$(obj_text).val(), n0=obj_text.selectionStart, n1=obj_text.selectionEnd;
		if (s.length==0) {return;}
		if (n0==n1) {$(obj_text).val(s0.substr(0,n0)+s+s0.substr(n0)); obj_text.selectionEnd=n1+s.length; obj_text.selectionStart=n0+s.length;}
		else if (s=='{}') {$(obj_text).val(s0.substr(0,n0)+'{'+s0.substr(n0,n1-n0)+'}'+s0.substr(n1)); obj_text.selectionEnd=n1+1; obj_text.selectionStart=n0+1;}
		else {$(obj_text).val(s0.substr(0,n0)+s+s0.substr(n1)); obj_text.selectionEnd=n1+s.length; obj_text.selectionStart=n0;}
		$(obj_text).trigger('input').focus();
		}
	radioBox(f_ok=(v_input)=>{console.log('radioBox',v_input);}, v_list={'N':'no selection list'}) {
		//let f_ok=(v_input)=>{console.log('radioBox',v_input);}, v_list={'DEL':'Delete item', 'COPY':'Copy to editor'};
		let w=400, h=50;
		let div0 =document.createElement('div'); //root w3-modal
		let div1 =document.createElement('div'); //w3-modal-content
		let div1a=document.createElement('div'); //w3-card
		let div2 =document.createElement('div'); //w3-display-topmiddle Message header
		let div2x=document.createElement('div'); //w3-display-topright w3-button
		let div3 =document.createElement('div'); //System Message/input ...
		let div4 =document.createElement('div'); //ok button div
		let btn0 =document.createElement('button');     //ok button
		$(div0).addClass('w3-modal').append(div1);
		$(div1).addClass('w3-modal-content w3-display-container').append(div1a).append(div2);
		$(div1a).addClass('w3-card');
		$(div2).height(40).width(w).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Action Box').css('padding-top','8px').css('margin','0')
			.append(div2x).append(div3).append(div4);
		$(div2x).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(div3).addClass('w3-white w3-left-align')
			.css('margin-top','15px').css('padding-top','20px').css('padding-left','100px')
			.css('min-width',w).css('min-height',h)
			;
		for (let k of Object.keys(v_list)) {//add radio input
			let obj0=document.createElement('input');
			let obj1=document.createElement('label');
			$(obj0).attr('type','radio').attr('name','action0').val(k).css('margin-right','5px');;
			$(obj1).text(v_list[k]).css('margin','10px');
			$(div3).append(obj0).append(obj1).append('<br>');
			}
		$(btn0).text('OK').css('margin',5).click((e)=>{
			f_ok($(e.target).parents('.w3-modal').find(':checked').val());
			$(e.target).parents('.w3-modal').remove();
			});
		$(div4).addClass('w3-center w3-white').css('padding','5px').append(btn0);

		$(document.body).append(div0);
		$(div0).show();
		} //inputBox
	tableBox(f_ok=(v_input)=>{console.log('tableBox',v_input);}) {
		let w=600, h=50;
		let div=(v_tag)=>{return document.createElement((v_tag)?v_tag:'div');}
		let DIVs=(n)=>{let x=[]; for (let i=0;i<n;i++) {x.push(div());} return x;}
		let createTable=(ncol=2, nrow=2)=>{
			let t0=div('table'), r;
			$(t0).addClass('w3-table w3-tiny w3-border w3-bordered').attr('contenteditable',true)
			.append($(div('caption')).text('Caption'))
			;
			r=div('colgroup'); for (let i=0;i<ncol;i++) {$(r).append($(div('col')))}
			$(t0).append(r);
			r=div('tr'); for (let i=0;i<ncol;i++) {$(r).append($(div('th')).text('C'+i))}
			$(t0).append(r);
			for (let j=0;j<nrow;j++) {
				let r=div('tr'); for (let i=0;i<ncol;i++) {$(r).append($(div('td')).text('R'+j+'C'+i))}
				$(t0).append(r);
				}
			return t0;
			}
		let d=DIVs(10);
		let btn0=div('button');
		$(d[0]).addClass('w3-modal').append(d[1]);
		$(d[1]).addClass('w3-modal-content w3-display-container').append(d[2]).append(d[3])
			.css('min-width',w);
		$(d[2]).addClass('w3-card');
		$(d[3]).height(40).addClass('w3-display-topmiddle w3-center w3-blue')
			.text('Table Editor').css('padding-top','8px').css('margin','0')
			.append(d[4]).append(d[5]);
		$(d[4]).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(d[5]).addClass('w3-white w3-left-align w3-center')
			.css('margin-top','15px').css('padding','20px')
			.css('min-width',w).css('min-height',h).append(d[6]).append(d[7]).append(btn0)
			;
		let ncol=div('input'), nrow=div('input');
		$(d[6]).addClass('w3-left').append(ncol).append(nrow);
		$(ncol).attr('type','number').addClass('w3-tiny').css('width','50px').val(2).attr('title','ncol')
		.change((e)=>{$(d[7]).empty().append(createTable($(ncol).val(),$(nrow).val()))})
		$(nrow).attr('type','number').addClass('w3-tiny').css('width','50px').val(2).attr('title','nrow')
		.change((e)=>{$(d[7]).empty().append(createTable($(ncol).val(),$(nrow).val()))})
		$(d[7]).empty().append(createTable())
		$(btn0).addClass('w3-tiny').text('OK').css('margin-top','10px');
		$(document.body).append(d[0]);
		$(d[0]).show();
		} //tableBox
	} //class LC_prompt
Date.prototype.format = function(s) {               // date format YYYY-MM-DD hh:mm:ss.fff+tz local timezone
	var mm = this.getMonth() + 1; // getMonth() is zero-based
	var dd = this.getDate();
	var hh = this.getHours();
	var mi = this.getMinutes();
	var ss = this.getSeconds();
	var ff = this.getMilliseconds()/1000;
	var tz = this.getTimezoneOffset();
	var f  = [this.getFullYear()
    	, '-', (mm>9 ? '' : '0') + mm
        , '-', (dd>9 ? '' : '0') + dd
        , ' ', (hh>9 ? '' : '0') + hh
        , ':', (mi>9 ? '' : '0') + mi
        , ':', (ss>9 ? '' : '0') + (ss+ff).toFixed(3)
        , (tz<=0 ? '+':'') + (-tz/60).toString()
		].join('');
	if (s=='val') {return this;}
	else if (s=='iso') {return this.toISOString();}
	else if (s=='str') {return this.toString();}
	else if (s=='tz') {return this.getTimezoneOffset();}
	else if (s=='hhmm') {return f.substr(11,5);}
	else {return f}
    return f;
    };
class LC_login {
	constructor() {
		this.url0='https://script.google.com/macros/s/AKfycbwzSMDlB6faBhW7YBtOIYeZeJ-nLE220K3w7XtyEkHNmqyVO1ITnVitWI9TL1Okm-bEQA/exec';
		this.login_user=null;
		this.login_dttm=null;
		this.login_credentials=null;
		this.session_id=null;
		this.f_login=()=>{};
		this.f_logout=()=>{};
		}
	div(v_tag){return document.createElement((v_tag)?v_tag:'div');}
	DIVs(n){let x=[]; for (let i=0;i<n;i++) {x.push(this.div());} return x;}
	modal(v_header,w,h){
		let d=this.DIVs(10); //root w3-modal(0) w3-modal-content(1) w3-card(2) w3-display-topmiddle(3) w3-display-topright(4) Content area(5)
		$(d[0]).addClass('w3-modal').append(d[1])
		$(d[1]).addClass('w3-modal-content w3-display-container').append(d[2]).append(d[3])
		$(d[2]).addClass('w3-card')
		$(d[3]).height(40).css('min-width',w).addClass('w3-display-topmiddle w3-center w3-green')
			.text(v_header).css('padding-top','10px').css('margin','0')
			.append(d[4]).append(d[5])
		$(d[4]).height(40).addClass('w3-display-topright w3-button w3-tiny').html('&times;')
			.css('padding','5').click((e)=>{$(e.target).parents('.w3-modal').remove();});
		$(d[5]).addClass('w3-center w3-white')
			.css('margin-top','10px').css('min-width',w).css('min-height',h)
		$(document.body).append(d[0])
		$(d[0]).show()
		return d[5];
		}
	login_box(){
		let w=400, h=100;
		let modal0=this.modal('User Login',w,h), input0=this.div('input'), pw0=this.div('input'), btn0 =this.div('button');
		let label0=this.div('label'), label1=this.div('label');
		$(modal0).append(input0).append('<br>').append(label0).append('<br>').append(pw0).append('<br>').append(label1).append('<br>').append(btn0)
		$(input0).addClass('w3-text-black w3-tiny')
			.width('50%').attr('placeholder','user login name').css('margin-top','30px')
		$(pw0).addClass('w3-text-black w3-tiny').attr('type','password')
			.width('50%').attr('placeholder','user password')
		$(label0).addClass('w3-text-red w3-tiny')
		$(label1).addClass('w3-text-red w3-tiny')
		$(btn0).addClass('w3-tiny').text('OK').css('margin',5).click((e)=>{
			this.login_user=null; this.login_dttm=null; this.login_credentials=null;
			let v1=$(input0).val(), v2=$(pw0).val();;
			if (v1.length<3) {$(label0).text('user name must be at least 3 char.');}
			else if (v2.length<6) {$(label1).text('password must be at least 6 char.');}
			else {this.server_login(v1,v2); $(e.target).parents('.w3-modal').remove();}
			})
		$(input0).focus()
		} // login_box()
	server_login(v_user,v_pw){console.log('send username/password to server');
		let v_params={'login_user':v_user, 'login_pw':v_pw};
		let callback0=(v, status)=>{
			console.log('status =',status, ', returnValue=',v);
			if (v.syserr) {this.message_box('Login failure: Server issue'); return -10;}
			else if (v.session_id==-1) {this.message_box('Login failure: Incorrect user name or password'); return -1;}
			else if (v.session_id>0) {
				this.login_user=v.login_user; this.login_dttm=v.login_dttm; this.login_credentials=v.login_user; this.session_id=v.session_id;
				// $('button').text(v.login_user);
				this.f_login();
				return this.message_box('Login successful: session ID='+v.session_id); 
				return v.session_id;}
			else {this.message_box('Login failure: Unknown issue'); return -100;}
			}
		$.getJSON(this.url0, v_params, callback0);
		} // server_login()
	set(f_name,f_run=()=>{}) {
		if (f_name=='f_login') this.f_login=f_run;
		if (f_name=='f_logout') this.f_logout=f_run;
		}
	message_box(v_msg){
		let w=400, h=100;
		let modal0=this.modal('Message',w,h);
		$(modal0).append($(this.div()).text(v_msg).css('padding-top','40px'));
		} // message_box
	nvl(v1,v2){if (v1) {return v1} else {return v2}}
	login_register(){//registrate new login user
		let w=400, h=200;
		let modal0=this.modal('New User Registration',w,h), user0=this.div('input'), pw0=this.div('input'), pw1=this.div('input')
			, ok0 =this.div('button'), check0=this.div(), d=this.DIVs(5);
		$(modal0).addClass('w3-tiny').append(d[0]).append(ok0)
		$(d[0]).append(d[1]).append(user0).append(check0).append('<br>').append(pw0).append('<br>')
			.append(pw1)
		$(d[0]).addClass('w3-left-align').css('padding',20).css('padding-left',80)
		$(d[1]).addClass('w3-text-red').html('&nbsp;') //system message
		$(user0).css('margin-left',10).attr('placeholder','new user name (at least 3 char)').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(pw0).attr('type','password').css('margin',10).attr('placeholder','new password (at least 6 char)').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(pw1).attr('type','password').css('margin',10).attr('placeholder','re-type new password').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(check0).addClass('w3-button').text('check').attr('title','check if user name available to apply')
			.click(()=>{// call server to validate if user not exist and available to add
			let v_params={'login_user_check':$(user0).val()};
			let callback0=(v,status)=>{console.log(v,status);
				let sysmsg=this.nvl(v['sysmsg'], 'Check failure: server issue');
				$(d[1]).html(sysmsg=='OK'?'User name available to register':sysmsg)
				};
			$.getJSON(this.url0, v_params, callback0);
			})
		$(ok0).text('OK').attr('title','click to add this user').css('margin-bottom',10).click(()=>{
			let chk1=()=>{if ($(user0).val().length<3) return 'user name must be at least 3 char'}
			let chk2=()=>{if ($(pw0).val().length<8) return 'password must be at least 6 char'}
			let chk3=()=>{if ($(pw0).val()!=$(pw1).val()) return 'retype password not match'}
			let sysmsg=this.nvl(chk1(),this.nvl(chk2(),chk3()));
			if (sysmsg) {$(d[1]).text(sysmsg); return}
			let v_params={'login_user_add':$(user0).val(),'login_pw':$(pw0).val()};
			let callback0=(v,status,xhr)=>{console.log(v,status);
				if (v.sysmsg) {this.message_box(v.sysmsg)}
				else {this.message_box('Process failure: server issue')}
				$(modal0).parents('.w3-modal').remove();
				}
			$.getJSON(this.url0, v_params, callback0);
			})
		} // login_register
	login_pw_modify(){//modify user password
		let w=400, h=200;
		let modal0=this.modal('Modify User Password',w,h), pw_old=this.div('input'), pw0=this.div('input'), pw1=this.div('input')
			, ok0 =this.div('button'), check0=this.div(), d=this.DIVs(5);
		$(modal0).addClass('w3-tiny').append(d[0]).append(ok0)
		$(d[0]).append(d[1]).append('Current User: '+this.login_user+'<br>').append(pw_old).append('<br>').append(pw0).append('<br>')
			.append(pw1)
		$(d[0]).addClass('w3-left-align').css('padding',20).css('padding-left',80)
		$(d[1]).addClass('w3-text-red').html('&nbsp;') //system message
		$(pw_old).attr('type','password').css('margin',10).attr('placeholder','original password').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(pw0).attr('type','password').css('margin',10).attr('placeholder','new password (at least 6 char)').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(pw1).attr('type','password').css('margin',10).attr('placeholder','re-type new password').attr('size',25)
			.on('input',(e)=>{$(d[1]).html('&nbsp;')})
		$(ok0).text('OK').attr('title','click to add this user').css('margin-bottom',10).click(()=>{
			let chk1=()=>{if ($(pw_old).val().length<6) return 'password must be at least 6 char'}
			let chk2=()=>{if ($(pw0).val().length<6) return 'password must be at least 6 char'}
			let chk3=()=>{if ($(pw0).val()!=$(pw1).val()) return 'retype password not match'}
			let sysmsg=this.nvl(chk1(),this.nvl(chk2(),chk3()));
			if (sysmsg) {$(d[1]).text(sysmsg); return}
			let v_params={'login_user_pw':this.login_user, 'login_pw_orig':$(pw_old).val(),'login_pw_new':$(pw0).val()};
			let callback0=(v,status,xhr)=>{console.log(v,status);
				if (v.sysmsg) {this.message_box(v.sysmsg)}
				else {this.message_box('Process failure: server issue')}
				$(modal0).parents('.w3-modal').remove();
				}
			$.getJSON(this.url0, v_params, callback0);
			})
		} // login_pw_modify
	login_menu(){//login menu
		let d=this.DIVs(5); //root w3-modal(0) w3-modal-content(1) w3-card(2) w3-display-topmiddle(3) w3-display-topright(4) Content area(5)
		$(d[0]).addClass('LOGIN_MENU w3-card w3-center w3-white w3-display-topright')
			.hover(null,(e)=>{$(d[0]).remove();})
		if (this.login_user) {
			$(d[0]).append(d[3]).append('<br>').append(d[4])
			$(d[3]).addClass('w3-button').text('Logout')
			$(d[4]).addClass('w3-button').text('Modify Password')
			} else {
			$(d[0]).append(d[1]).append('<br>').append(d[2])
			$(d[1]).addClass('w3-button').text('Login now')
			$(d[2]).addClass('w3-button').text('Register new user')
			}
		$(d[3]).click(()=>{$(d[0]).remove();this.logout();})
		$(d[4]).click(()=>{$(d[0]).remove();this.login_pw_modify();})
		$(d[1]).click(()=>{$(d[0]).remove();this.login_box();})
		$(d[2]).click(()=>{$(d[0]).remove();this.login_register();})
		$(document.body).append(d[0])
		$(d[0]).show()
		return d[5];
		} // login_menu
	logout(){
		this.login_user=null; this.login_dttm=null; this.login_credentials=null; this.session_id=null;
		//$('button').text('login');
		this.f_logout();
		} // logout
	/*/login0=new LC_login();
	//login0.login_box();
	//login0.login_register();
	login0=new LC_login();
	// login0.login_menu();
	console.log(new Date().format());
	let btn0=document.createElement('button');
	$(document.body).append($(btn0).addClass('w3-right').text('Login').click(()=>{login0.login_menu()}))
	*/
	} //LC_login

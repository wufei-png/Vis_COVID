import Globe from 'globe.gl';
import { request, getCoordinates, numberWithCommas, formatDate } from './utils';
import {
  GLOBE_IMAGE_URL,
  BACKGROUND_IMAGE_URL,
  GEOJSON_URL,
  // GEOJSON_URL2,
  CASES_API,
} from './constants';
import * as d3 from 'd3';
import * as echarts from 'echarts';
import * as jquery from 'jquery';
var view_index=0;
var current_order
var child_get_order=(element)=>{
  //console.log("这是第",)
  var i=0;
  while( (element = element.previousSibling) != null ) 
      i++;
  //console.log("这是第",i,'个');
  return i;
}
// var change_view=(order)=>{

// }
// var init_change_button=()=>{
//   var buttons=document.getElementsByClassName('change_view_button');
//   for (let i = 0; i < buttons.length; i++) {
//     //console.log("typeof(Deletes[i])",Deletes[i]);
//     buttons[i].setAttribute('index',i);
//     buttons[i].addEventListener("click", change_view_handle);
// }
// }
// var change_view_handle=function(){
//   // console.log("typeof(element)",this);
//   change_view_handle_this(this);//this传参，比较重要的知识点
// }
// var change_view_handle_this=(element)=>{
//   // var order=child_get_order(element);
//   console.log('element',element)
//   var order=Number(element.getAttribute('index'));
//   console.log('order',(order));//这里为什么不对
//   change_view(order);
// }

var st_global=()=>{
// Globe container
const globeContainer = document.getElementById('globeViz');
var speed_slider=200;
const SPEED_MAX=500;
const SPEED_MIN=25;

let dates = [];
let countries = [];
let featureCollection = [];
let featureCollection2 = [];


const colorScale = d3.scaleSequentialPow(d3.interpolateYlOrRd).exponent(1 / 4);
const getVal = (feat) => {
  return feat.covidData.confirmed / feat.properties.POP_EST; //确诊除以人口
};

let world;
let flagName;
const flagEndpoint = 'https://corona.lmao.ninja/assets/img/flags';
// Play button
const playButton = document.querySelector('.play-button');
// Slider
const slider = document.querySelector('.slider');
// Slider date
const sliderDate = document.querySelector('.slider-date');
let interval;
var setclock=()=>{
  clearInterval(interval);
  interval = setInterval(() => {
    slider.value++;
    sliderDate.innerHTML = dates[slider.value];
    updateCounters();
    updatePolygonsData();
    show_hisgram();
    show_die();
    if (+slider.value === dates.length - 1) {
      playButton.innerHTML = 'Play';
      clearInterval(interval);
    }
  }, speed_slider);
}
var init_speed_button=()=>{
  var buttons=document.getElementsByClassName('speed');
  for (let i = 0; i < buttons.length; i++) {
    //console.log("typeof(Deletes[i])",Deletes[i]);
    buttons[i].setAttribute('index',i);
    buttons[i].addEventListener("click", speed_handle);
}
}
var speed_handle=function(){
  // console.log("typeof(element)",this);
  speed_handle_this(this);//this传参，比较重要的知识点
}
var speed_handle_this=(element)=>{
  // var order=child_get_order(element);
  console.log('element',String(element.innerHTML)=='+')
  if(String(element.innerHTML)=='+'){
      if(speed_slider>SPEED_MIN)
      {   
          //console.log('speed_slider min',speed_slider)
          speed_slider-=25;
      }
    }
  else if(speed_slider<SPEED_MAX)
  {
    //console.log('speed_slider max',speed_slider)
    speed_slider+=25;
  }
  // var order=Number(element.getAttribute('index'));
  // console.log('order',(order));//这里为什么不对
  // change_view(order);
  console.log('speed_slider',speed_slider)
  if(playButton.innerText == 'Pause')//实时更新
  {
    setclock();
  }
}

function show_hisgram() {
  var option = {
      backgroundColor: 'rgba(207,176,18,0)',
      title: {
          text: "全球累计确诊国家TOP10",
          padding:[20,0,0,40],
          textStyle: {
              color:'white',
          },
          left: 'left'
      },
      color: ['#db3333'],
      tooltip: {
          trigger: 'axis',
          //指示器
          axisPointer: {
              type: 'shadow'  //默认为直线，可选为： ‘line’ | 'shadow'
          },
          formatter: function(params){
              var res;
              //console.log('params',params)
              res= '<div>'+name_to_fullname[params[0].name]+':'+params[0].value+'</div>';
              return res
          }


      },
      xAxis: {
          tpye: 'category',
          data: [],
          axisLabel:
              {
                color:'white',
              }
      },
      yAxis: {
          type: 'value',
          //y轴字体设置
          axisLabel: {
              show: true,
              color:'white',

              fontSize: 12,
              formatter: function (value) {//数据过大
                      value = value / 10000000 + 'kw';
                      return value;
              }
          },
      },


      series: [{
          data: [],//[582,300,100],
          type: 'bar',
          barMaxWidth: "50%"
      }
    ]
  };
  // for (let x = 0; x < featureCollection.length; x++) {
  //   const country = featureCollection[x].properties.NAME;
  //   if (countries[country]) {
  //     featureCollection[x].covidData = {//把读入的json添加一个新属性 covidData
  //       confirmed: countries[country][dates[slider.value]].confirmed,
  //       deaths: countries[country][dates[slider.value]].deaths,//这是data.json里的
  //       recoveries: countries[country][dates[slider.value]].recoveries,
  //     };
  var topData = [];

  for (let x = 0; x < featureCollection.length; x++) {
      // console.log(  'name',featureCollection[x].properties.NAME,
      // 'value',featureCollection[x].covidData.confirmed)
      topData.push({
        // d.ISO_A2.toLowerCase()
          'name': featureCollection[x].properties.ISO_A2.toLowerCase()=='-99'?'fr':featureCollection[x].properties.ISO_A2.toLowerCase(),
          'value': featureCollection[x].covidData.confirmed,
          'fullname': featureCollection[x].properties.NAME
      });
  }
  
  //降序排列
  topData.sort(function (a, b) {
      return b.value - a.value;
  });
  //只保留前10个
  topData.length = 10;
  var name_to_fullname={};
  for (let x = 0; x < topData.length; x++) {
    name_to_fullname[topData[x].name]=topData[x].fullname
  }

  console.log('name_to_fullname',name_to_fullname);
  //分别取出省份名称和数值
  // console.log('topData',topData)
  for (var country of topData) {
      option.xAxis.data.push(country.name);
      option.series[0].data.push(country.value);
      // option.series[0].data.push(country.fullname);
  }
  histogram.setOption(option);
}//全球累计确诊地区TOP10(柱形图)
function show_die() {
  var option = {

      backgroundColor: 'rgba(166,207,18,0)',
      title: {
          text: '现有确诊国家TOP10',
          left: 'center',
          textStyle:{
              fontSize:20,
              fontWeight:'bold',
              fontFamily:'Microsoft YaHei',
              color:'#000'
          },
      },
      tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        padding: [100,0,0,0],
          orient: 'vertical',
          left: 'right',
          data: [],
      },
      series: [
          {
              name: '国家名称',
              type: 'pie',
              radius: '55%',
              data: [],
              emphasis: {
                  itemStyle: {

                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0,0,0,0)'
                  }
              }
          }
      ]
  };

  var topData = [];
  for (let x = 0; x < featureCollection.length; x++) {
    // console.log(  'name',featureCollection[x].properties.NAME,
    // 'value',featureCollection[x].covidData.confirmed)
    topData.push({
      // d.ISO_A2.toLowerCase()
        //'name': featureCollection[x].properties.ISO_A2.toLowerCase()=='-99'?'fr':featureCollection[x].properties.ISO_A2.toLowerCase(),
        'name': featureCollection[x].properties.NAME,
        'value': featureCollection[x].covidData.confirmed,
    });
}
  //降序的排列
  topData.sort(function (a, b) {
      return b.value - a.value;
  });
  //只保留前几个
  topData.length = 10;
  //分别取出省份名称和数据
  for (var country of topData) {
      option.legend.data.push(country.name);
      option.series[0].data.push(country);
  }
  //console.log(topData);
  die.setOption(option);
}//现有确诊地区TOP15(扇形图)

var histogram = echarts.init(document.getElementById('histogram'), 'dark');
var die = echarts.init(document.getElementById('die'), 'dark');
init();

function init() {
  world = Globe()(globeContainer)
    .globeImageUrl(GLOBE_IMAGE_URL)
    .backgroundImageUrl(BACKGROUND_IMAGE_URL)
    .showGraticules(false)//获取器/设置器，用于是否显示以每 10 度划分纬度和经度线的刻度网格。
    .polygonAltitude(0.06)//初始化动画
    .polygonCapColor((feat) => colorScale(getVal(feat)))//?
    .polygonSideColor(() => 'rgba(0, 100, 0, 0.05)')//?
    .polygonStrokeColor(() => '#111')
    .polygonLabel(({ properties: d, covidData: c }) => {
      if (d.ADMIN === 'France') {
        flagName = 'fr';
      } else if (d.ADMIN === 'Norway') {
        flagName = 'no';
      } else {
        flagName = d.ISO_A2.toLowerCase();
      }
//hover显示国旗等信息
      return `
        <div class="card">
          <img class="card-img" src="${flagEndpoint}/${flagName}.png" alt="flag" />
          <div class="container">
             <span class="card-title"><b>${d.NAME}</b></span> <br />
             <div class="card-spacer"></div>
             <hr />
             <div class="card-spacer"></div>
             <span>Cases: ${numberWithCommas(c.confirmed)}</span>  <br />
             <span>Deaths: ${numberWithCommas(c.deaths)}</span> <br />
             <span>Recovered: ${numberWithCommas(c.recoveries)}</span> <br />
             <span>Population: ${d3.format('.3s')(d.POP_EST)}</span>
          </div>
        </div>
      `;
    })
    .onPolygonHover((hoverD) =>
      world
        .polygonAltitude((d) => (d === hoverD ? 0.12 : 0.06))
        .polygonCapColor((d) =>
          d === hoverD ? 'steelblue' : colorScale(getVal(d))
        )
    )
    .polygonsTransitionDuration(200);
  getCases();//调用这个更新时间跨度
  // init_change_button();
  init_speed_button();
  // console.log('featureCollection',featureCollection)
  // //show_hisgram();
}




function polygonFromCenter(center, radius=0.5, num=10) {
  let coords = [];
  for (let i = 0; i < num; i++) {
    const dx = radius*Math.cos(2*Math.PI*i/num);
    const dy = radius*Math.sin(2*Math.PI*i/num);
    coords.push([center[0] + dx, center[1] + dy]);
  }
  return [coords];
}

async function getCases() {
  countries = await request(CASES_API);
  featureCollection = (await request(GEOJSON_URL)).features;//地图数据

  // featureCollection2 = (await request(GEOJSON_URL2)).features.map(d => {
  //   d.geometry.type = "Polygon";
  //   d.geometry.coordinates = polygonFromCenter(d.geometry.coordinates);
  //   return d;
  // });
  // featureCollection = featureCollection.concat(featureCollection2);

  // world.polygonsData(countriesWithCovid);
  document.querySelector('.title-desc').innerHTML =
    'Hover on a country or territory to see cases, deaths, and recoveries.';

  dates = Object.keys(countries.China);

  // Set slider values
  slider.max = dates.length - 1;
  slider.value = dates.length - 1;//进度条

  slider.disabled = false;//为1无法拖动
  playButton.disabled = false;

  updateCounters();
  updatePolygonsData();
  
  updatePointOfView();
  show_hisgram();
  show_die();
  //console.log('featureCollection inner',featureCollection)
}

const infectedEl = document.querySelector('#infected');
const deathsEl = document.querySelector('#deaths');
const recoveriesEl = document.querySelector('#recovered');
const updatedEl = document.querySelector('.updated');
function updateCounters() {//更新底部信息
  sliderDate.innerHTML = dates[slider.value];

  let totalConfirmed = 0;
  let totalDeaths = 0;
  let totalRecoveries = 0;

  Object.keys(countries).forEach((item) => {
    if (countries[item][dates[slider.value]]) {
      const countryDate = countries[item][dates[slider.value]];
      totalConfirmed += +countryDate.confirmed;
      totalDeaths += +countryDate.deaths;
      totalRecoveries += countryDate.recoveries ? +countryDate.recoveries : 0;
    }
  });

  infectedEl.innerHTML = numberWithCommas(totalConfirmed);
  deathsEl.innerHTML = numberWithCommas(totalDeaths);
  recoveriesEl.innerHTML = numberWithCommas(totalRecoveries);

  updatedEl.innerHTML = `(as of ${formatDate(dates[slider.value])})`;
}

function updatePolygonsData() {
  for (let x = 0; x < featureCollection.length; x++) {
    const country = featureCollection[x].properties.NAME;
    if (countries[country]) {
      featureCollection[x].covidData = {//把读入的json添加一个新属性 covidData
        confirmed: countries[country][dates[slider.value]].confirmed,
        deaths: countries[country][dates[slider.value]].deaths,//这是data.json里的
        recoveries: countries[country][dates[slider.value]].recoveries,
      };
    } else {
      featureCollection[x].covidData = {
        confirmed: 0,
        deaths: 0,
        recoveries: 0,
      };
    }
  }

  const maxVal = Math.max(...featureCollection.map(getVal));
  colorScale.domain([0, maxVal]);//设置domain
  world.polygonsData(featureCollection);//这一句更新实际的图
  // console.log('featureCollection inner inner',featureCollection)
}

async function updatePointOfView() {//初始化页面的显示位置，自己的ip地址
  // Get coordinates
  try {
    const { latitude, longitude } = await getCoordinates();

    world.pointOfView(
      {
        lat: latitude,//纬度
        lng: longitude,//经度
      },
      1000
    );
  } catch (e) {
    console.log('Unable to set point of view.');
  }
}


playButton.addEventListener('click', () => {
  if (playButton.innerText === 'Play') {
    playButton.innerText = 'Pause';
  } else {
    playButton.innerText = 'Play';
    clearInterval(interval);
    return;
  }

  // Check if slider position is max
  if (+slider.value === dates.length - 1) {
    slider.value = 0;//在刚点击的时候是不是为最大值
  }

  sliderDate.innerHTML = dates[slider.value];

  setclock();
});

if ('oninput' in slider) {//指针滑动时间轴
  // console.log(666)
  slider.addEventListener(
    'input',
    function () {
      updateCounters();
      updatePolygonsData();
      show_hisgram();
      show_die();
    },
    false
  );
}

// Responsive globe
window.addEventListener('resize', (event) => {
  // console.log("success");
  world.width([event.target.innerWidth]);
  world.height([event.target.innerHeight]);
});
}
st_global();




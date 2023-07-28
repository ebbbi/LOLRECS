"use client";

import styles from "./champreader.module.css";
import React, { useState, useRef } from "react";

function ChampReader({ bans, allies, enemies }) {
  const videoRef = useRef();
  const canvasRef = useRef();
  const [screenSharing, setScreenSharing] = useState(false);
  const [localStream, setLocalStream] = useState(null);
  const [showTooltip, setShowTooltip] = useState(false);

  const startScreenSharing = async () => {
    if (localStream) {
      localStream.getTracks().forEach((track) => track.stop());
    }

    try {
      let stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
      setLocalStream(stream);
    } catch (error) {
      console.error("Error accessing screen sharing:", error);
    }
  };

  const stopScreenSharing = () => {
    if (localStream) {
      localStream.getTracks().forEach((track) => track.stop());
      videoRef.current.load();
      setLocalStream(null);
    }
  };

  const controlScreenSharing = () => {
    if (screenSharing) {
      stopScreenSharing();
      setScreenSharing(false);
    } else {
      startScreenSharing();
      setScreenSharing(true);
    }
  };

  const [banpickResult, setbanpickresult] = useState([]);
  const submitScreenShot = () => {
    canvasRef.current.width = videoRef.current.videoWidth;
    canvasRef.current.height = videoRef.current.videoHeight;
    canvasRef.current
      .getContext("2d")
      .drawImage(
        videoRef.current,
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );

    fetch(`https://www.lolrecs.com/api/recognize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        image: canvasRef.current.toDataURL("image/png"),
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        return response.json();
      })
      .then((data) => {
        data = data["banpicList"];
        console.log(data);
        bans.map((ban, i) => {
          ban[1](data[i]);
        });
        allies.map((ally, i) => {
          ally[1](data[i + 10]);
        });
        enemies.map((enemy, i) => {
          enemy[1](data[i + 15]);
        });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className={styles.buttonArea}>
      <div className={styles.buttonContainer}>
        <video ref={videoRef} style={{ display: "none" }} />
        <canvas ref={canvasRef} style={{ display: "none" }} />
        <button
          className={`${styles.picCapButton} ${
            screenSharing ? styles.stopSharing : styles.startSharing
          }`}
          onClick={controlScreenSharing}
        >
          {screenSharing ? "화면 공유 중단" : "화면 공유 시작"}
        </button>
        <button
          className={styles.picCapButton}
          onClick={submitScreenShot}
          disabled={!screenSharing}
        >
          화면 인식 하기
        </button>
      </div>
      <div className={styles.toolTip}>
        <button
          className={styles.tooltipButton}
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <i className="bi bi-info-circle" />
        </button>
        {showTooltip && (
          <>
            <span className={styles.tooltipArticleNoPC}>
              <p>pc환경에서만 실시간 화면 인식 기능을 사용하실 수 있습니다.</p>
            </span>
            <span className={styles.tooltipArticle}>
              <p>본인 픽 차례일 때,</p>
              <p>'화면 공유 시작'</p>
              <p>↓</p>
              <p>롤 화면 선택</p>
              <p>↓</p>
              <p>'화면 인식 하기' (1번만 클릭)</p>
              <p>↓</p>
              <p>'화면 공유 중단'</p>
              <div className={styles.tolltipSpecial}>
                * 최소 1명의 픽이 인식되어야 추천 서비스를 받으실 수 있습니다.
              </div>
            </span>
          </>
        )}
      </div>
    </div>
  );
}

export default ChampReader;

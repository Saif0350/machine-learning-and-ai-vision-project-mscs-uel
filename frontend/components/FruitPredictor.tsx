"use client";

import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { ImagePlus, Sparkles, UploadCloud, X, Loader2 } from "lucide-react";
import { message } from "antd";
import SinglePredictionTab from "./SinglePredictionTab";
import MultiplePredictionTab from "./MultiplePredictionTab";
import { useRef } from "react";

const backend = process.env.NEXT_PUBLIC_BACKEND;

type PredictionResult = {
  id: string;
  file: File;
  preview: string;
  fruit: string | null;
  confidence: number | null;
  loading: boolean;
  error: string | null;
};

const tabs = [
  { key: "single", label: "Single Image" },
  { key: "multiple", label: "Multiple Images" },
];

export default function FruitPredictor() {
  const [activeTab, setActiveTab] = useState<"single" | "multiple">("single");

  const [singleFile, setSingleFile] = useState<File | null>(null);
  const [singlePreview, setSinglePreview] = useState<string | null>(null);
  const [singleFruit, setSingleFruit] = useState<string | null>(null);
  const [singleConfidence, setSingleConfidence] = useState<number | null>(null);
  const [singleLoading, setSingleLoading] = useState(false);
  const [singleInputKey, setSingleInputKey] = useState(0);
  const singleInputRef = useRef<HTMLInputElement | null>(null);
  const [multiItems, setMultiItems] = useState<PredictionResult[]>([]);
  const [batchLoading, setBatchLoading] = useState(false);

  useEffect(() => {
    return () => {
      if (singlePreview) URL.revokeObjectURL(singlePreview);
      multiItems.forEach((item) => URL.revokeObjectURL(item.preview));
    };
  }, [singlePreview, multiItems]);

  const stats = useMemo(() => {
    const predicted = multiItems.filter(
      (item) => item.fruit && !item.error,
    ).length;
    return {
      total: multiItems.length,
      predicted,
    };
  }, [multiItems]);

  const validateImage = (file: File) => {
    if (!file.type.startsWith("image/")) {
      message.error(`${file.name} is not a valid image file.`);
      return false;
    }
    return true;
  };

  const handleSingleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      message.error("Please select a valid image file.");
      return;
    }

    setSingleFile(file);
    setSingleFruit(null);
    setSingleConfidence(null);

    setSinglePreview((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return URL.createObjectURL(file);
    });
  };

  const handleMultipleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []).filter(validateImage);
    if (!files.length) return;

    const newItems: PredictionResult[] = files.map((file) => ({
      id: `${file.name}-${file.size}-${Date.now()}-${Math.random()}`,
      file,
      preview: URL.createObjectURL(file),
      fruit: null,
      confidence: null,
      loading: false,
      error: null,
    }));

    setMultiItems((prev) => [...prev, ...newItems]);
  };

  const predictSingleFile = async (file: File) => {
    if (!backend) {
      throw new Error(
        "Backend URL is missing. Check NEXT_PUBLIC_BACKEND in .env.local",
      );
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${backend}/predict`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return {
      fruit: res.data?.fruit || res.data?.class || "Unknown",
      confidence:
        typeof res.data?.confidence === "number"
          ? parseFloat(res.data.confidence.toFixed(2))
          : null,
    };
  };

  const handlePredictSingle = async () => {
    if (!singleFile) {
      message.warning("Please upload an image first.");
      return;
    }

    try {
      setSingleLoading(true);
      const result = await predictSingleFile(singleFile);
      setSingleFruit(result.fruit);
      setSingleConfidence(result.confidence);
    } catch (error: any) {
      message.error(
        error?.response?.data?.detail || error?.message || "Prediction failed.",
      );
    } finally {
      setSingleLoading(false);
    }
  };

  const handlePredictMultiple = async () => {
    if (!multiItems.length) {
      message.warning("Please upload at least one image.");
      return;
    }

    if (!backend) {
      message.error(
        "Backend URL is missing. Check NEXT_PUBLIC_BACKEND in .env.local",
      );
      return;
    }

    setBatchLoading(true);

    for (const item of multiItems) {
      setMultiItems((prev) =>
        prev.map((p) =>
          p.id === item.id ? { ...p, loading: true, error: null } : p,
        ),
      );

      try {
        const result = await predictSingleFile(item.file);

        setMultiItems((prev) =>
          prev.map((p) =>
            p.id === item.id
              ? {
                  ...p,
                  fruit: result.fruit,
                  confidence: result.confidence,
                  loading: false,
                  error: null,
                }
              : p,
          ),
        );
      } catch (error: any) {
        setMultiItems((prev) =>
          prev.map((p) =>
            p.id === item.id
              ? {
                  ...p,
                  loading: false,
                  error:
                    error?.response?.data?.detail ||
                    error?.message ||
                    "Prediction failed",
                }
              : p,
          ),
        );
      }
    }

    setBatchLoading(false);
  };

  const handleSingleReset = () => {
    if (singlePreview) {
      URL.revokeObjectURL(singlePreview);
    }

    setSingleFile(null);
    setSinglePreview(null);
    setSingleFruit(null);
    setSingleConfidence(null);

    if (singleInputRef.current) {
      singleInputRef.current.value = "";
    }

    setSingleInputKey((prev) => prev + 1);
  };

  const removeMultiItem = (id: string) => {
    setMultiItems((prev) => {
      const found = prev.find((item) => item.id === id);
      if (found) URL.revokeObjectURL(found.preview);
      return prev.filter((item) => item.id !== id);
    });
  };

  const clearAllMulti = () => {
    multiItems.forEach((item) => URL.revokeObjectURL(item.preview));
    setMultiItems([]);
  };

  return (
    <section className="min-h-screen bg-[#f6f8f4] px-4 py-10 md:px-8">
      <div className="mx-auto templateContainer">
        <div className="mb-10">
          <p className="mb-3 flex items-center gap-2 text-sm uppercase tracking-[0.18em] text-gray-500">
            <Sparkles size={16} />
            Fruit AI Classifier
          </p>

          <h1 className="max-w-3xl text-3xl font-medium leading-tight text-[#111] md:text-5xl">
            Clean, fast, and intuitive fruit prediction experience
          </h1>

          <p className="mt-4 max-w-2xl text-sm leading-7 text-gray-600 md:text-base">
            Upload one image for a focused prediction or switch to multiple
            images for batch classification. The UI is designed to feel simple,
            modern, and easy to scan.
          </p>
        </div>

        <div className="rounded-[28px] border border-black/5 bg-white p-4 shadow-[0_10px_40px_rgba(0,0,0,0.05)] md:p-6">
          {/* Tabs */}
          <div className="mb-8 flex flex-wrap gap-2">
            {tabs.map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setActiveTab(tab.key as "single" | "multiple")}
                className={`relative rounded-full px-5 py-2.5 text-sm transition-all duration-300 ${
                  activeTab === tab.key
                    ? "bg-[#1f2937] text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {activeTab === "single" ? (
              <motion.div
                key="single"
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                transition={{ duration: 0.3 }}
              >
                <SinglePredictionTab
                  singlePreview={singlePreview}
                  singleFile={singleFile}
                  singleFruit={singleFruit}
                  singleConfidence={singleConfidence}
                  singleLoading={singleLoading}
                  inputRef={singleInputRef}
                  inputKey={singleInputKey}
                  onUpload={handleSingleUpload}
                  onPredict={handlePredictSingle}
                  onReset={handleSingleReset}
                />
              </motion.div>
            ) : (
              <motion.div
                key="multiple"
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                transition={{ duration: 0.3 }}
              >
                <MultiplePredictionTab
                  multiItems={multiItems}
                  batchLoading={batchLoading}
                  stats={stats}
                  onUpload={handleMultipleUpload}
                  onPredictAll={handlePredictMultiple}
                  onClearAll={clearAllMulti}
                  onRemoveItem={removeMultiItem}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}

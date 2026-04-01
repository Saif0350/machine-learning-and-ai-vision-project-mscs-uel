"use client";

import { Loader2, UploadCloud, X } from "lucide-react";
import { motion } from "framer-motion";
import Image from "next/image";

type MultiItem = {
  id: string;
  file: File;
  preview: string;
  fruit: string | null;
  confidence: number | null;
  loading: boolean;
  error: string | null;
};

type Stats = {
  total: number;
  predicted: number;
};

type MultiplePredictionTabProps = {
  multiItems: MultiItem[];
  batchLoading: boolean;
  stats: Stats;
  onUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onPredictAll: () => void;
  onClearAll: () => void;
  onRemoveItem: (id: string) => void;
};

export default function MultiplePredictionTab({
  multiItems,
  batchLoading,
  stats,
  onUpload,
  onPredictAll,
  onClearAll,
  onRemoveItem,
}: MultiplePredictionTabProps) {
  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <h2 className="text-xl font-medium text-[#111]">
            Multiple image prediction
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Upload several fruit images and classify them one by one with the
            same endpoint.
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <label className="cursor-pointer rounded-full bg-gray-100 px-5 py-3 text-sm font-medium text-gray-700 transition hover:bg-gray-200">
            Add Images
            <input
              type="file"
              accept="image/*"
              multiple
              className="hidden"
              onChange={onUpload}
            />
          </label>

          <button
            type="button"
            onClick={onPredictAll}
            disabled={batchLoading || !multiItems.length}
            className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-green-600 via-emerald-700 to-green-600 px-5 py-3 text-sm font-medium text-white transition-all duration-300 hover:from-green-600 hover:via-emerald-600 hover:to-green-700 hover:shadow-lg active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {batchLoading ? "Predicting..." : "Predict All"}
          </button>

          {!!multiItems.length && (
            <button
              type="button"
              onClick={onClearAll}
              className="rounded-full bg-red-50 px-5 py-3 text-sm font-medium text-red-600 transition hover:bg-red-100"
            >
              Clear All
            </button>
          )}
        </div>
      </div>

      <div className="grid gap-4 rounded-[24px] border border-gray-200 bg-[#fafaf8] p-4 md:grid-cols-3">
        <div className="rounded-2xl bg-white p-4">
          <p className="text-sm text-gray-500">Total Images</p>
          <p className="mt-2 text-2xl font-semibold text-[#111]">
            {stats.total}
          </p>
        </div>
        <div className="rounded-2xl bg-white p-4">
          <p className="text-sm text-gray-500">Predicted</p>
          <p className="mt-2 text-2xl font-semibold text-[#111]">
            {stats.predicted}
          </p>
        </div>
        <div className="rounded-2xl bg-white p-4">
          <p className="text-sm text-gray-500">Mode</p>
          <p className="mt-2 text-2xl font-semibold text-[#111]">Batch</p>
        </div>
      </div>

      {multiItems.length === 0 ? (
        <label className="flex min-h-[280px] cursor-pointer flex-col items-center justify-center rounded-[24px] border-2 border-dashed border-gray-300 bg-[#fafafa] px-6 text-center transition-all duration-300 hover:border-green-500 hover:bg-green-50/40">
          <input
            type="file"
            accept="image/*"
            multiple
            className="hidden"
            onChange={onUpload}
          />
          <div className="mb-4 rounded-full bg-green-100 p-4 text-green-700">
            <UploadCloud size={28} />
          </div>
          <p className="text-base font-medium text-[#111]">
            Upload multiple fruit images
          </p>
          <p className="mt-2 text-sm text-gray-500">
            Build a clean prediction gallery for batch analysis
          </p>
        </label>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-6">
          {multiItems.map((item, index) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04 }}
              className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm"
            >
              <div className="relative">
                <Image
                  width={1000}
                  height={1000}
                  src={item.preview}
                  alt={item.file.name}
                  className="h-30 w-full object-contain"
                />
                <button
                  type="button"
                  onClick={() => onRemoveItem(item.id)}
                  className="absolute right-3 top-3 rounded-full bg-white/90 p-2 text-gray-700 shadow hover:bg-black hover:text-white"
                >
                  <X size={16} />
                </button>
              </div>

              <div className="p-4">
                <p className="truncate text-sm font-medium text-[#111]">
                  {item.file.name}
                </p>

                <div className="mt-4 min-h-[40px]">
                  {item.loading ? (
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Loader2 size={16} className="animate-spin" />
                      Predicting...
                    </div>
                  ) : item.error ? (
                    <p className="text-sm text-red-500">{item.error}</p>
                  ) : item.fruit && item.confidence !== null ? (
                    <div>
                      <p className="text-lg font-semibold text-[#111]">
                        {item.fruit}
                      </p>
                      <div className="mt-3">
                        <div className="mb-2 flex items-center justify-between text-xs text-gray-500">
                          <span>Confidence</span>
                          <span>{item.confidence}%</span>
                        </div>
                        <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-200">
                          <div
                            className="h-full rounded-full bg-green-600"
                            style={{ width: `${item.confidence}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-400">
                      Waiting for prediction
                    </p>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
